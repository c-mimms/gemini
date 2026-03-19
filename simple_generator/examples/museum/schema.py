from pydantic import BaseModel, Field

class MuseumArticle(BaseModel):
    title: str = Field(description="A catchy title for the article")
    description: str = Field(description="A 1-2 sentence compelling summary of the output.")
    tag: str = Field(description="Format Name | Theme, e.g., 'Deep Dive | Hardware'")
    format_used: str = Field(description="The exact name of the format chosen from the instructions (e.g., 'The Deep Dive Narrative').")
    topic_or_artifact: str = Field(description="The name of the chosen artifact, person, company, or theme.")
    html_content: str = Field(description="The full HTML content using the provided CSS Tool Inventory. Do not wrap in <main>.")
    image_urls_to_download: list[str] = Field(
        default_factory=list,
        description="A list of Wikimedia Commons Special:FilePath URLs to download for this article."
    )
