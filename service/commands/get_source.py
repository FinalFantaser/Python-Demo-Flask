import urllib.parse

class GetSource:
    _DIRECT_ENTRY = 'DIRECT_ENTRY'
    _validated_data: dict

    def __init__(self, validated_data: dict):
        self._validated_data = validated_data
    # Конструктор

    def run(self) -> str:
        if self._validated_data['referrer'] is not None:
            parsed = urllib.parse.urlparse(url=self._validated_data['referrer'])
            return parsed['hostname']
        elif self._validated_data['url_query_string'] is None:
            return self._DIRECT_ENTRY
        elif self._validated_data['utm_source'] is not None:
            return self._validated_data['utm_source']
        else:
            return self._DIRECT_ENTRY
    # run
