from typing import List
from pydantic import BaseModel, Field


class SocialMediaPost(BaseModel):
    """
    Representa un post individual adaptado para una red social específica.
    """
    platform: str = Field(
        ...,
        description="Plataforma de destino (ej. 'Twitter/X', 'LinkedIn', 'Instagram')."
    )
    content: str = Field(
        ...,
        description="Texto completo del post, incluyendo hashtags, emojis pertinentes y menciones."
    )


class ContentOutput(BaseModel):
    """
    Esquema final entregable por el Quality Assurance Agent.
    Agrupa el artículo principal y la suite de publicaciones para redes sociales.
    """
    article: str = Field(
        ...,
        description="El artículo de análisis o blog post completo, formateado rigurosamente en Markdown."
    )
    social_media_posts: List[SocialMediaPost] = Field(
        ...,
        description="Lista de posts optimizados para cada plataforma social correspondiente al artículo."
    )