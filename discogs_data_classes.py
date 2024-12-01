from datetime import datetime


class RecordItem:

    def __init__(
            self,
            release_id: int,
            item_id: int,
            available: int,
            url: str,
            adjusted_price: float,
            media_condition: str,
            sleeve_condition: str,
            details: str,
            avg_rating: float,
            num_ratings: int,
            country: str,
            date_created: datetime,
            date_updated: datetime

    ) -> object:
        self.release_id = release_id
        self.item_id = item_id
        self.available = available
        self.url = url
        self.adjusted_price = adjusted_price
        self.media_condition = media_condition
        self.sleeve_condition = sleeve_condition
        self.details = details
        self.avg_rating = avg_rating
        self.num_ratings = num_ratings
        self.country = country
        self.date_created = date_created
        self.date_updated = date_updated

    # Not necessary. Can just use .__dict__
    # def to_dict(self):
    #     return {
    #         'release_id': self.release_id,
    #         'item_id': self.item_id,
    #         'available': self.available,
    #         'url': self.url,
    #         'adjusted_price': self.adjusted_price,
    #         'media_condition': self.media_condition,
    #         'sleeve_condition': self.sleeve_condition,
    #         'details': self.details,
    #         'avg_rating': self.avg_rating,
    #         'num_ratings': self.num_ratings,
    #         'country': self.country,
    #         'date_created': self.date_created,
    #         'date_updated': self.date_updated
    #     }


class RecordMaster:

    def __init__(
            self,
            master_id: int,
            master_url: str,
            artist: str,
            title: str,
            formats: str,
            year: int,
            country: str,
            date_created: datetime,
            date_updated: datetime,
            num_items: int = -1,
            min_price: float = -1.0,
            desired_price: float = 100,
            last_scrape_date: datetime = datetime.min
    ):
        self.master_id: int = master_id
        self.master_url: str = master_url
        self.artist: str = artist
        self.title: str = title
        self.formats: str = formats
        self.year: int = year
        self.country: str = country
        self.date_created = date_created
        self.date_updated = date_updated
        self.num_items = num_items
        self.min_price = min_price
        self.desired_price=desired_price
        self.last_scrape_date = last_scrape_date


class ScrapeQueue:

    def __init__(
            self,
            row_id: int,
            batch_id: int,
            master_id: int,
            artist: str,
            title: str,
            formats: str,
            status: str,
            date_updated: datetime

    ):
        self.row_id: int = row_id
        self.batch_id: int = batch_id
        self.master_id: int = master_id
        self.artist: str = artist
        self.title: str = title
        self.formats: str = formats
        self.status: str = status
        self.date_updated: datetime = date_updated
