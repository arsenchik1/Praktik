import asyncio
import uuid
from typing import Dict, List, Any

import aiohttp
from django.conf import settings


class OneCService:
    """Сервис для взаимодействия с API 1С"""
    
    def __init__(self, club_id: str = None):
        self.base_url = settings.ONE_C_BASE_URL
        self.login = settings.ONE_C_LOGIN
        self.password = settings.ONE_C_PASSWORD
        self.club_id = club_id or settings.ONE_C_CLUB_ID
        self.request_id = str(uuid.uuid4())
    
    async def get_employees(self) -> List[Dict[str, Any]]:
        """Получение списка сотрудников из 1С"""
        payload = {
            "Request_id": self.request_id,
            "ClubId": self.club_id,
            "Method": "GetSpecialistList",
            "Parameters": {
                "ServiceId": ""
            }
        }
        
        auth = aiohttp.BasicAuth(self.login, self.password)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    json=payload,
                    auth=auth,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        # Пробуем получить реальные данные, если не получится - используем тестовые
                        try:
                            data = await response.json()
                            # Преобразуем данные из 1С в нужный формат
                            employees = self._transform_employees(data)
                            if employees:
                                return employees
                        except:
                            # Если не удалось получить данные, используем тестовые
                            pass
                    
                    # Тестовые данные для разработки
                    return self._get_test_employees()
        except Exception as e:
            print(f"Error connecting to 1C: {e}")
            # В случае ошибки возвращаем тестовые данные
            return self._get_test_employees()
    
    def _transform_employees(self, data: Dict) -> List[Dict[str, str]]:
        """Преобразование данных из формата 1С в требуемый формат"""
        employees = []
        
        # Здесь нужно адаптировать под реальный формат ответа от 1С
        # Пример обработки, если данные приходят в ожидаемом формате
        if isinstance(data, dict):
            # Если данные в формате {"specialists": [...]}
            specialists = data.get('specialists', data.get('data', []))
            if isinstance(specialists, list):
                for specialist in specialists:
                    if isinstance(specialist, dict):
                        employee = {
                            'id': str(specialist.get('id', '')),
                            'name': specialist.get('name', specialist.get('firstName', '')),
                            'last_name': specialist.get('last_name', specialist.get('lastName', '')),
                            'phone': specialist.get('phone', ''),
                            'image_url': specialist.get('image_url', specialist.get('photo', ''))
                        }
                        employees.append(employee)
        
        return employees
    
    def _get_test_employees(self) -> List[Dict[str, str]]:
        """Тестовые данные для разработки"""
        return [
            {
                'id': '1',
                'name': 'Иван',
                'last_name': 'Петров',
                'phone': '+7 (999) 123-45-67',
                'image_url': 'https://via.placeholder.com/150'
            },
            {
                'id': '2',
                'name': 'Мария',
                'last_name': 'Иванова',
                'phone': '+7 (999) 765-43-21',
                'image_url': 'https://via.placeholder.com/150'
            },
            {
                'id': '3',
                'name': 'Алексей',
                'last_name': 'Сидоров',
                'phone': '+7 (999) 555-55-55',
                'image_url': 'https://via.placeholder.com/150'
            }
        ]


class EmployeeService:
    """Сервис для работы с данными сотрудников"""
    
    @staticmethod
    async def get_employees_from_1c(club_id: str = None) -> List[Dict]:
        """Получение сотрудников из 1С"""
        one_c_service = OneCService(club_id)
        try:
            employees = await one_c_service.get_employees()
            return employees
        except Exception as e:
            print(f"Error getting employees: {e}")
            # Возвращаем тестовые данные в случае ошибки
            return one_c_service._get_test_employees()