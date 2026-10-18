from pydantic import BaseModel, ConfigDict, Field, field_validator


class IndicatorInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=3, max_length=160)
    definition: str = Field(min_length=10, max_length=3000)
    domain: str | None = Field(default=None, max_length=100)
    unit: str = Field(min_length=1, max_length=60)
    dimensions: list[str] = Field(default_factory=list, max_length=20)

    @field_validator("dimensions")
    @classmethod
    def valid_dimensions(cls, values):
        if any(not v.strip() or len(v) > 100 for v in values) or len(set(values)) != len(values):
            raise ValueError("Dimensiones vacías, duplicadas o demasiado largas")
        return values

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
    active: bool | None = None
    dimensions: list[str] | None = Field(default=None, max_length=20)

    @field_validator("active", "dimensions")
    @classmethod
    def non_null_options(cls, value):
        if value is None:
            raise ValueError("No puede establecerse como nulo")
        if isinstance(value, list) and (any(not v.strip() or len(v) > 100 for v in value) or len(set(value)) != len(value)):
            raise ValueError("Dimensiones inválidas")
        return value

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
    active: bool
    dimensions: list[str]


class IndicatorPage(BaseModel):
    items: list[IndicatorView]
    total: int
    limit: int
    offset: int
