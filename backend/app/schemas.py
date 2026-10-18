from pydantic import BaseModel, ConfigDict, Field, field_validator


class IndicatorInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=3, max_length=160)
    definition: str = Field(min_length=10, max_length=3000)
    domain: str | None = Field(default=None, max_length=100)
    unit: str = Field(min_length=1, max_length=60)

    @field_validator("domain")
    @classmethod
    def empty_domain_is_none(cls, v: str | None) -> str | None:
        return v or None


class IndicatorPatch(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=3, max_length=160)
    definition: str | None = Field(default=None, min_length=10, max_length=3000)
    domain: str | None = Field(default=None, max_length=100)
    unit: str | None = Field(default=None, min_length=1, max_length=60)

    @field_validator("name", "definition", "unit")
    @classmethod
    def must_not_be_null(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("No puede establecerse como nulo")
        return value


class IndicatorView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    code: str
    name: str
    definition: str
    domain: str | None
    unit: str
    status: str
    created_at: str
    updated_at: str


class IndicatorPage(BaseModel):
    items: list[IndicatorView]
    total: int
    limit: int
    offset: int
