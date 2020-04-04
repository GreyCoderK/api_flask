from sqlalchemy import Column, DATETIME, INTEGER, String, TEXT, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app import db

class BaseModel(db.Model):

    __abstract__ = True
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    created_at = Column(DATETIME(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DATETIME(timezone=True), nullable=True, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class TypeUser(BaseModel):

    __tablename__ = "type_user"

    libelle = Column(String(150), index=True, unique=True)
    users = relationship('Users', backref='type_user', lazy='dynamic')

    def __repr__(self):
        return f'<TypeArticle {self.libelle}>'


class TypeArticle(BaseModel):

    __tablename__ = "type_article"

    libelle = Column(String(150), index=True, unique=True)
    articles = relationship('Articles', backref='type_article', lazy='dynamic')

    def __repr__(self):
        return f'<TypeArticle {self.libelle}>'


class User(BaseModel):

    __tablename__ = "user"

    name = Column(String(64), index=True, unique=True)
    mail = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))
    articles = relationship('Article', backref='author', lazy='dynamic')
    type_user_id = Column(INTEGER, ForeignKey('type_user.id'), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'


class Article(BaseModel):

    __tablename__ = "article"

    reference = Column(String(150), index=True, unique=True)
    libelle = Column(String(150), index=True, unique=True)
    image = Column(String(150))
    detail = Column(TEXT)
    prix = Column(INTEGER, index=True)
    type_article_id = Column(INTEGER, ForeignKey('type_article.id'), nullable=False)
    user_id = Column(INTEGER, ForeignKey('user.id'), nullable=True)
    
    def __repr__(self):
        return  f"""
                    <Article {self.libelle}> : reference {self.reference}
                                   prix {self.prix}
                                   detail : {self.detail}
                    <TypeArticle {self.type_article_id}>
                    <Auteur {self.user_id}>                
                """


class MenuVertical(BaseModel):

    __tablename__ = "menu_vertical"

    libelle = Column(String(128), index=True, unique=True)
    icone = Column(String(60))
    couleur = Column(String(28))

    def __repr__(self):
        return f'<MenuVertical {self.libelle}>'

