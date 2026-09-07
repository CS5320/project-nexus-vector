import re

from .errors import ValidationError


class CustomerValidationPolicy:
    """Central validation policy introduced but not adopted everywhere."""

    EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def validate_name(self, name: str | None) -> str:
        if name is None or len(name.strip()) < 2:
            raise ValidationError("customer name must contain at least two characters")
        return name.strip()

    def validate_email(self, email: str | None) -> str:
        candidate = (email or "").strip().lower()
        if not self.EMAIL_PATTERN.match(candidate):
            raise ValidationError("customer email is invalid")
        return candidate

    def validate_tag(self, tag: str | None) -> str:
        cleaned = (tag or "").strip().lower()
        if not cleaned:
            raise ValidationError("tag may not be empty")
        if len(cleaned) > 30:
            raise ValidationError("tag may not exceed 30 characters")
        return cleaned
