import uuid

from rest_framework import response, status
from rest_framework.views import APIView

from chatapp import controllers, serializers


class ChatHistory(APIView):
    def post(self, request):
        user = request.user
        thread_id = request.data.get("chat_thread_id", None)
        user_query = request.data.get("user_query", None)

        char_history_controller = controllers.ChatHistoryController()

        # Check if user_query is provided
        if not user_query:
            return response.Response(
                {
                    "result": False,
                    "msg": "User query not provided.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If no thread_id is provided, create a new thread
        if not thread_id:
            chat_thread = char_history_controller.create_thread(
                user=user, query=user_query, is_active=False
            )
        else:
            # Validate the thread_id format
            try:
                uuid.UUID(thread_id)
            except ValueError:
                return response.Response(
                    {
                        "result": False,
                        "msg": "Invalid thread ID format.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Retrieve the existing chat thread
            chat_thread = char_history_controller.get_thread(
                user=user, thread_id=thread_id
            )

            # Mock the chat response based on the user query
            chat_response = char_history_controller.mockchat(user_query)

            # Save the chat history
            add_history = char_history_controller.save_chat_history(
                chat_thread=chat_thread,
                query=user_query,
                response=chat_response,
            )

            # Serialize the added chat history
            serialized_data = serializers.ChatHistorySerializers(
                add_history
            ).data

            return response.Response(
                {"result": True, "msg": "Success", "data": serialized_data},
                status=status.HTTP_201_CREATED,
            )

    def get(self, request, thread_id=None):
        user = request.user
        chat_history_controller = controllers.ChatHistoryController()

        # Fetch chat history based on the thread_id
        chat_history_data = chat_history_controller.get_chat_history(
            user=user, thread_id=thread_id
        )

        # Serialize the retrieved chat history
        serialized_data = serializers.ChatHistorySerializers(
            chat_history_data
        ).data

        return response.Response(
            {"result": True, "msg": "Success", "data": serialized_data},
            status=status.HTTP_200_OK,
        )


class ChatBookmark(APIView):
    def get(self, request):
        user = request.user
        search_text = request.query_params.get("search_text", None)
        char_history_controller = controllers.ChatHistoryController()

        if search_text:
            chat_data = char_history_controller.search_bookmark(
                user=user, search_text=search_text
            )
        else:
            chat_data = char_history_controller.get_bookmark(user=user)
        serialized_data = serializers.ChatHistorySerializers(chat_data).data

        return response.Response(
            {"result": True, "msg": "success", "data": serialized_data}
        )

    def put(self, request):
        chat_id = request.data.get("chat_id", None)
        is_bookmark = request.data.get("is_bookmarked", False)
        char_history_controller = controllers.ChatHistoryController()

        data = char_history_controller.bookmark_chat_history(
            chat_id=chat_id, is_bookmark=is_bookmark
        )

        return response.Response(
            {
                "result": True,
                "msg": f"Successfully set bookmark to {is_bookmark}",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )


class ChatThread(APIView):
    def get(self, request):
        char_history_controller = controllers.ChatHistoryController()
        user = request.user
        search_text = request.query_params.get("search_text", None)

        if search_text:
            chat_thread = char_history_controller.search_chat_thread(
                user=user, search_text=search_text
            )
        else:
            chat_thread = char_history_controller.get_all_threads(user=user)

            return response.Response(
                {"result": True, "msg": "good", "data": chat_thread}
            )
