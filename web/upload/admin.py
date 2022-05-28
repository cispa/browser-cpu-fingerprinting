from django.contrib import admin
from .models import BenchmarkResult

# admin.site.register(BenchmarkResult)
@admin.register(BenchmarkResult)
class BenchmarkResultAdmin(admin.ModelAdmin):
    #list_display = ("model", "show_pagesize", "show_prefetcher", "show_cacheasso", "show_cachesizesmall", "show_cachesizelarge", "show_tlbsize", "show_timertime", "show_timerdiff", "show_memory", "show_loadbuffer", "show_singleperf", "show_multiperf", "show_cores")
    list_display = ("model", "user_agent")

    def show_pagesize(self, obj):
        from django.utils.html import format_html
        return format_html("<img style='height: 100px' src='data:image/png;base64,{}'>", obj.b64_charts[0])

    show_pagesize.short_description = "Pagesize"

    def show_prefetcher(self, obj):
        from django.utils.html import format_html
        return format_html("<img style='height: 100px' src='data:image/png;base64,{}'>", obj.b64_charts[1])

    show_prefetcher.short_description = "Prefetcher"

    def show_cacheasso(self, obj):
        from django.utils.html import format_html
        return format_html("<img style='height: 100px' src='data:image/png;base64,{}'>", obj.b64_charts[2])

    show_cacheasso.short_description = "Cache associativity"

    def show_cachesizesmall(self, obj):
        from django.utils.html import format_html
        return format_html("<img style='height: 100px' src='data:image/png;base64,{}'>", obj.b64_charts[3])

    show_cachesizesmall.short_description = "Cache size small"

    def show_cachesizelarge(self, obj):
        from django.utils.html import format_html
        return format_html("<img style='height: 100px' src='data:image/png;base64,{}'>", obj.b64_charts[4])

    show_cachesizelarge.short_description = "Cache size large"

    def show_tlbsize(self, obj):
        from django.utils.html import format_html
        return format_html("<img style='height: 100px' src='data:image/png;base64,{}'>", obj.b64_charts[5])

    show_tlbsize.short_description = "TLB size"

    def show_timertime(self, obj):
        from django.utils.html import format_html
        return format_html("<img style='height: 100px' src='data:image/png;base64,{}'>", obj.b64_charts[6])

    show_timertime.short_description = "Timer /time"

    def show_timerdiff(self, obj):
        from django.utils.html import format_html
        return format_html("<img style='height: 100px' src='data:image/png;base64,{}'>", obj.b64_charts[7])

    show_timerdiff.short_description = "Timer /diff"

    def show_memory(self, obj):
        from django.utils.html import format_html
        return format_html("<img style='height: 100px' src='data:image/png;base64,{}'>", obj.b64_charts[8])

    show_memory.short_description = "Memory"

    def show_loadbuffer(self, obj):
        from django.utils.html import format_html
        return format_html("<img style='height: 100px' src='data:image/png;base64,{}'>", obj.b64_charts[9])

    show_loadbuffer.short_description = "LB size"

    def show_singleperf(self, obj):
        from django.utils.html import format_html
        return format_html("<img style='height: 100px' src='data:image/png;base64,{}'>", obj.b64_charts[10])

    show_singleperf.short_description = "Single perf"

    def show_multiperf(self, obj):
        from django.utils.html import format_html
        return format_html("<img style='height: 100px' src='data:image/png;base64,{}'>", obj.b64_charts[11])

    show_multiperf.short_description = "Multi perf"

    def show_cores(self, obj):
        from django.utils.html import format_html
        return format_html("<img style='height: 100px' src='data:image/png;base64,{}'>", obj.b64_charts[12])

    show_cores.short_description = "Cores"

