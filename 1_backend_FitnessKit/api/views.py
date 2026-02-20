from rest_framework.views import APIView
from rest_framework.response import Response
import httpx
import uuid
from django.conf import settings

class GetEmployeesView(APIView):

    async def get(self, request):
        # Prepare request body
        request_id = str(uuid.uuid4())
        body = {
            "Request_id": request_id,
            "ClubId": settings.EXTERNAL_CLUB_ID,
            "Method": "GetSpecialistList",
            "Parameters": {
                "ServiceId": ""
            }
        }

        headers = {
            'Content-Type': 'application/json'
        }

        # Выполнение асинхронного POST-запроса
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.EXTERNAL_API_URL,
                json=body,
                headers=headers,
                auth=(settings.EXTERNAL_LOGIN, settings.EXTERNAL_PASSWORD)
            )

        # Обработка ответа
        if response.status_code != 200:
            return Response({"error": "Failed to fetch data from external system"}, status=500)

        data = response.json()

        # Предполагаемый формат ответа (нужно уточнить, если есть пример)
        # Для примера возьмем, что data содержит список сотрудников в ключе 'Employees'
        employees = data.get('Employees', [])

        result = []
        for emp in employees:
            result.append({
                "id": emp.get("id", ""),
                "name": emp.get("name", ""),
                "last_name": emp.get("last_name", ""),
                "phone": emp.get("phone", ""),
                "image_url": emp.get("image_url", "")
            })

        return Response(result)
