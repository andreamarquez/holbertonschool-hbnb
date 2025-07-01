from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def get_reviews_by_place(self, place_id):
        return self.model.query.filter_by(place=place_id).all()

    def get_reviews_by_user(self, user_id):
        return self.model.query.filter_by(user=user_id).all()
