from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class GetEmployeesView(APIView):
    """
    Простая рабочая версия с заглушкой
    """
    
    def get(self, request):
        # Заглушка для демонстрации
        employees = [
            {
                "id": "1",
                "name": "Иван",
                "last_name": "Иванов",
                "phone": "+7 (999) 123-45-67",
                "image_url": "https://via.placeholder.com/150"
            },
            {
                "id": "2",
                "name": "Петр",
                "last_name": "Петров",
                "phone": "+7 (999) 765-43-21",
                "image_url": "https://via.placeholder.com/150"
            },
            {
                "id": "3",
                "name": "Сергей",
                "last_name": "Сергеев",
                "phone": "+7 (999) 555-55-55",
                "image_url": "https://via.placeholder.com/150"
            }
        ]
        return Response(employees)