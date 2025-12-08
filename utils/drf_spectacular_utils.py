from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes

def ordering_parameter(fields: list[str]):
    return OpenApiParameter(
        name='ordering',
        type=OpenApiTypes.STR,
        description=(
            f"Ordering of results. Use comma-separated fields. "
            f"Prefix with `-` for descending order.\n"
            f"Allowed fields: {', '.join(fields)}"
        ),
        required=False,
    )