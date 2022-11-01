from rest_framework.metadata import SimpleMetadata


class MinimalMetadata(SimpleMetadata):
    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        return metadata
