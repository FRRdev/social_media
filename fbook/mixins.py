from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage


class PageMixin:
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_users = self.get_queryset()
        print(list_users)
        paginator = Paginator(list_users, PageMixin.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context['users_list'] = file_exams
        return context