from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator


class CountrySchema(BaseModel):
    country: str


class GenreSchema(BaseModel):
    genre: str


class MovieShortDetailSchema(BaseModel):
    film_id: int = Field(alias="filmId")
    name_ru: Optional[str] = Field(None, alias="nameRu")
    type: Optional[str] = Field(None, alias="type")
    year: Optional[int] = Field(None, alias="year")
    description: Optional[str] = Field(None, alias="description")
    film_length: Optional[str] = Field(None, alias="filmLength")
    countries: Optional[List[CountrySchema]] = Field(None, alias="countries")
    genres: Optional[List[GenreSchema]] = Field(None, alias="genres")
    rating: Optional[str] = Field(None, alias="rating")
    rating_vote_count: Optional[int] = Field(None, alias="ratingVoteCount")
    poster_url: Optional[HttpUrl] = Field(None, alias="posterUrl")
    poster_url_preview: Optional[HttpUrl] = Field(None, alias="posterUrlPreview")


class MovieDetailSchema(BaseModel):
    kinopoisk_id: int = Field(alias="kinopoiskId")
    kinopoisk_hd_id: Optional[int] = Field(None, alias="kinopoiskHDId")
    imdb_id: Optional[str] = Field(None, alias="imdbId")
    name_ru: Optional[str] = Field(None, alias="nameRu")
    name_en: Optional[str] = Field(None, alias="nameEn")
    name_original: Optional[str] = Field(None, alias="nameOriginal")
    poster_url: Optional[HttpUrl] = Field(None, alias="posterUrl")
    poster_url_preview: Optional[HttpUrl] = Field(None, alias="posterUrlPreview")
    cover_url: Optional[HttpUrl] = Field(None, alias="coverUrl")
    logo_url: Optional[HttpUrl] = Field(None, alias="logoUrl")
    reviews_count: Optional[int] = Field(None, alias="reviewsCount")
    rating_good_review: Optional[float] = Field(None, alias="ratingGoodReview")
    rating_good_review_vote_count: Optional[int] = Field(
        None, alias="ratingGoodReviewVoteCount"
    )
    rating_kinopoisk: Optional[float] = Field(None, alias="ratingKinopoisk")
    rating_kinopoisk_vote_count: Optional[int] = Field(
        None, alias="ratingKinopoiskVoteCount"
    )
    rating_imdb: Optional[float] = Field(None, alias="ratingImdb")
    rating_imdb_vote_count: Optional[int] = Field(None, alias="ratingImdbVoteCount")
    rating_film_critics: Optional[float] = Field(None, alias="ratingFilmCritics")
    rating_film_critics_vote_count: Optional[int] = Field(
        None, alias="ratingFilmCriticsVoteCount"
    )
    rating_await: Optional[float] = Field(None, alias="ratingAwait")
    rating_await_count: Optional[int] = Field(None, alias="ratingAwaitCount")
    rating_rf_critics: Optional[float] = Field(None, alias="ratingRfCritics")
    rating_rf_critics_vote_count: Optional[int] = Field(
        None, alias="ratingRfCriticsVoteCount"
    )
    web_url: Optional[HttpUrl] = Field(None, alias="webUrl")
    year: Optional[int] = Field(None, alias="year")
    film_length: Optional[int] = Field(None, alias="filmLength")
    slogan: Optional[str] = Field(None, alias="slogan")
    description: Optional[str] = Field(None, alias="description")
    short_description: Optional[str] = Field(None, alias="shortDescription")
    editor_annotation: Optional[str] = Field(None, alias="editorAnnotation")
    is_tickets_available: Optional[bool] = Field(None, alias="isTicketsAvailable")
    production_status: Optional[str] = Field(None, alias="productionStatus")
    type: Optional[str] = Field(None, alias="type")
    rating_mpaa: Optional[str] = Field(None, alias="ratingMpaa")
    rating_age_limits: Optional[str] = Field(None, alias="ratingAgeLimits")
    countries: Optional[List[CountrySchema]] = Field(None, alias="countries")
    genres: Optional[List[GenreSchema]] = Field(None, alias="genres")
    start_year: Optional[int] = Field(None, alias="startYear")
    end_year: Optional[int] = Field(None, alias="endYear")
    serial: Optional[bool] = Field(None, alias="serial")
    short_film: Optional[bool] = Field(None, alias="shortFilm")
    completed: Optional[bool] = Field(None, alias="completed")
    has_imax: Optional[bool] = Field(None, alias="hasImax")
    has_3d: Optional[bool] = Field(None, alias="has3D")
    last_sync: Optional[datetime] = Field(None, alias="lastSync")


class SeachMoviesByKeywordSchema(BaseModel):
    query: str = Field(None, validation_alias="keyword")
    films: list[MovieShortDetailSchema]

    @field_validator("films", mode="before")
    @classmethod
    def validate_films(cls, v):
        if isinstance(v, list):
            return [MovieShortDetailSchema.model_validate(film) for film in v]
        return v
