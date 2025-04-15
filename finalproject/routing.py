from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from analytics.consumers import MetricsConsumer,AllTimeMacrosConsumer,WeeklyMacrosConsumer,MonthlyMacrosConsumer

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("ws/metrics/", MetricsConsumer.as_asgi()),
        path('ws/all_time_macros/', AllTimeMacrosConsumer.as_asgi()),
        path("ws/weekly_macros/", WeeklyMacrosConsumer.as_asgi()),
        path("ws/monthly_macros/", MonthlyMacrosConsumer.as_asgi())
    ])
})


