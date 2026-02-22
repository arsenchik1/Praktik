import logging
import asyncio
from django.http import JsonResponse
from django.views import View
from django.core.cache import cache

from .services import EmployeeService

logger = logging.getLogger(__name__)


class GetEmployeesView(View):
    """Представление для получения списка сотрудников"""
    
    def get(self, request, *args, **kwargs):
        """Синхронная обработка GET запроса с асинхронным вызовом внутри"""
        try:
            club_id = request.GET.get('club_id')
            cache_key = f'employees_{club_id or "default"}'
            
            # Проверка кэша
            cached_data = cache.get(cache_key)
            if cached_data:
                return JsonResponse({'employees': cached_data, 'cached': True})
            
            # Асинхронный вызов сервиса в синхронном контексте
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                employees = loop.run_until_complete(
                    EmployeeService.get_employees_from_1c(club_id)
                )
            finally:
                loop.close()
            
            # Кэширование на 5 минут
            cache.set(cache_key, employees, 300)
            
            return JsonResponse({'employees': employees})
            
        except Exception as e:
            logger.error(f"Error in GetEmployeesView: {e}", exc_info=True)
            return JsonResponse(
                {'error': 'Failed to fetch employees', 'details': str(e)},
                status=500
            )