from drf_yasg import openapi
def get_queryfield(filed,required=True):
    return openapi.Parameter(
            name=filed,
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            required=required,  # Set to True if it's required
            description=filed
        )