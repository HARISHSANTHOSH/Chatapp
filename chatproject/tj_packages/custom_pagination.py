import typing

from django.contrib import auth
from django.db.models import QuerySet
from rest_framework import serializers

User = auth.get_user_model()


class Pagination:
    def get_paginated_response(
        self,
        queryset: QuerySet,
        offset: int,
        limit: int,
        Serializer: serializers.Serializer,
    ) -> typing.Tuple[dict, bool]:
        try:
            offset = int(offset)
            previous_limit = int(limit)
        except ValueError:
            raise serializers.ValidationError(
                {"result": False, "msg": "Limit or offset should be numbers"},
                code="validation_error",
            )
        try:
            limit = offset + previous_limit + 1
            queryset_data = queryset[int(offset) : limit]  # noqa
            serializer_data = Serializer(queryset_data, many=True)
        except IndexError as e:
            raise serializers.ValidationError(str(e))
        if len(queryset_data) > previous_limit:
            next_link = True
            serialized_data = serializer_data.data[:-1]
        else:
            next_link = False
            serialized_data = serializer_data.data
        return serialized_data, next_link

    def get_web_paginated_response(
        self,
        queryset: QuerySet,
        offset: int,
        limit: int,
        Serializer: typing.Type[serializers.Serializer],
    ) -> typing.Tuple[dict, bool, int]:
        try:
            offset = int(offset)
            previous_limit = int(limit)
        except ValueError:
            raise serializers.ValidationError(
                {"result": False, "msg": "Limit or offset should be numbers"},
                code="validation_error",
            )
        try:
            total_count = queryset.count()
            limit = offset + previous_limit + 1
            queryset_data = queryset[int(offset) : limit]  # noqa
            serializer_data = Serializer(queryset_data, many=True)
        except IndexError as e:
            raise serializers.ValidationError(str(e))
        if len(queryset_data) > previous_limit:
            next_link = True
            serialized_data = serializer_data.data[:-1]
        else:
            next_link = False
            serialized_data = serializer_data.data
        return serialized_data, next_link, total_count

    def get_web_paginated_response_with_previous_and_next_link(
        self,
        queryset: QuerySet,
        offset: int,
        limit: int,
        Serializer: typing.Type[serializers.Serializer],
    ) -> typing.Tuple[list[dict], bool, bool, int]:
        """Returns a paginated and serialized response based on given offset and limit.
        Supports both previous_link and next_link.

        Args:
            queryset: Django Queryset to which pagination needs to be applied.
            offset: integer value for the start index of the pagination.
            limit: max results per page.
            serializer: Serializer class to be used for JSON serialization.

        Returns:
            list[dict]: List of dictionaries for the paginated and serialized elements.
            bool: Indicates whether previous page is present based on current offset.
            bool: Indicates whether next page is present based on current offset, limit and count on Queryset.
            int: Total count from the Queryset.
        """
        try:
            offset = int(offset)
            previous_limit = int(limit)
        except ValueError:
            raise serializers.ValidationError(
                {"result": False, "msg": "Limit or offset should be numbers"},
                code="validation_error",
            )
        total_count = queryset.count()
        limit = offset + previous_limit + 1
        try:
            queryset_data = queryset[int(offset) : limit]  # noqa
            serializer_data = Serializer(queryset_data, many=True)
        except IndexError as e:
            raise serializers.ValidationError(str(e))

        if len(queryset_data) > previous_limit:
            next_link = True
            serialized_data = serializer_data.data[:-1]
        else:
            next_link = False
            serialized_data = serializer_data.data
        previous_link = offset > 0
        return serialized_data, previous_link, next_link, total_count

    def get_web_user_paginated_response(
        self,
        user: User,
        queryset: QuerySet,
        offset: int,
        limit: int,
        Serializer: serializers.Serializer,
    ) -> typing.Tuple[dict, bool]:
        try:
            offset = int(offset)
            previous_limit = int(limit)
        except ValueError:
            raise serializers.ValidationError(
                {"result": False, "msg": "Limit or offset should be numbers"},
                code="validation_error",
            )
        try:
            if int(offset) == 0:
                total_count = queryset.count()
            else:
                total_count = queryset.count()
            limit = offset + previous_limit + 1
            queryset_data = queryset[int(offset) : limit]  # noqa
            serializer_data = Serializer(
                queryset_data, many=True, context={"user_id": user.id}
            )
        except IndexError as e:
            raise serializers.ValidationError(str(e))
        if len(queryset_data) > previous_limit:
            next_link = True
            serialized_data = serializer_data.data[:-1]
        else:
            next_link = False
            serialized_data = serializer_data.data
        return serialized_data, next_link, total_count

    def get_by_web_paginated_response(
        self,
        queryset: QuerySet,
        offset: int,
        limit: int,
        Serializer: serializers.Serializer,
    ) -> typing.Tuple[dict, bool]:
        try:
            offset = int(offset)
            previous_limit = int(limit)
        except ValueError:
            raise serializers.ValidationError(
                {"result": False, "msg": "Limit or offset should be numbers"},
                code="validation_error",
            )
        try:
            if int(offset) == 0:
                total_count = queryset.count()  # noqa
            else:
                total_count = None  # noqa
            limit = offset + previous_limit + 1
            queryset_data = queryset[int(offset) : limit]  # noqa
            serializer_data = Serializer(queryset_data, many=True)
        except IndexError as e:
            raise serializers.ValidationError(str(e))
        if len(queryset_data) > previous_limit:
            next_link = True
            serialized_data = serializer_data.data[:-1]
        else:
            next_link = False
            serialized_data = serializer_data.data
        return serialized_data, next_link

    def get_paginated_response_extra_args(
        self,
        queryset: QuerySet,
        offset: int,
        limit: int,
        Serializer: serializers.Serializer,
        extra_args={},
    ) -> typing.Tuple[dict, bool]:
        try:
            offset = int(offset)
            previous_limit = int(limit)
        except ValueError:
            raise serializers.ValidationError(
                {"result": False, "msg": "Limit or offset should be numbers"},
                code="validation_error",
            )
        try:
            limit = offset + previous_limit + 1
            queryset_data = queryset[int(offset) : limit]  # noqa
            if not extra_args:
                serializer_data = Serializer(queryset_data, many=True)
            else:
                serializer_data = Serializer(
                    queryset_data, many=True, context=extra_args
                )
        except IndexError as e:
            raise serializers.ValidationError(str(e))
        if len(queryset_data) > previous_limit:
            next_link = True
            serialized_data = serializer_data.data[:-1]
        else:
            next_link = False
            serialized_data = serializer_data.data
        return serialized_data, next_link
