# views.py
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from tools.constant import ERROR_500,bad_request,sucess,PAGE_NOT_FOUND
from .models import Book
from .serializers import BookSerializer
from tools.swagger import get_queryfield
from rest_framework import status
from django.db.models import Q
import logging
logger = logging.getLogger(__name__)




class MyPagination(PageNumberPagination):
    page_size = 25  # Default page size
    max_page_size = 25
    def get_page_count(self):
        return self.page.paginator.num_pages
    
    def get_current_page(self):
        return self.page.number


class BookListAPIView(ListAPIView):
    serializer_class = BookSerializer
    pagination_class = MyPagination

    @swagger_auto_schema( 
        operation_summary="Get list of books with filter options",
        manual_parameters=[get_queryfield('book_id',required=False),get_queryfield('language',required=False),get_queryfield('mime_type',required=False),
                                             get_queryfield('topic',required=False),get_queryfield('author',required=False),
                                             get_queryfield('title',required=False)],
       
        responses={
            '200': openapi.Response(description=sucess),
            '400': openapi.Response(description=bad_request),
        })
    def get(self, request, *args, **kwargs):
        try:
            res_data = {}
            queryset = Book.objects.filter(~Q(title=None)).prefetch_related('authors', 'languages', 'subjects', 'bookshelves')
            
            # Filters
            gutenberg_id = request.GET.get('book_id')
            if gutenberg_id:
                gutenberg_ids = gutenberg_id.split(",")
                queryset = queryset.filter(gutenberg_id__in=gutenberg_ids)
            language = request.GET.get('language')
            if language:
                languages = [l.strip() for l in language.split(',') if l.strip()]
                queryset = queryset.filter(languages__code__in=languages)

            mime_type = request.GET.get('mime_type')
            if mime_type:
                mime_types = [m.strip() for m in mime_type.split(',') if m.strip()]
                queryset = queryset.filter(format__mime_type__in=mime_types)

            topic = request.GET.get('topic')
            if topic:
                keywords = [a.strip() for a in topic.split(',') if a.strip()]
                topic_filter = Q()
                for t in keywords:
                    topic_filter |= Q(subjects__name__icontains=t) | Q(bookshelves__name__icontains=t)
                queryset = queryset.filter(topic_filter)

            author = request.GET.get('author')
            if author:
                keywords = [a.strip() for a in author.split(',') if a.strip()]
                author_filter = Q()
                for a in keywords:
                    author_filter |= Q(authors__name__icontains=a)
                queryset = queryset.filter(author_filter)

            title = request.GET.get('title')
            if title:
                keywords = [t.strip() for t in title.split(',') if t.strip()]
                title_filter = Q()
                for t in keywords:
                    title_filter |= Q(title__icontains=t)
                queryset = queryset.filter(title_filter)


            # Sort by popularity
            queryset = queryset.order_by('-download_count').distinct()
            paginator = MyPagination()
            try:
                result_page = paginator.paginate_queryset(queryset, request)
            except Exception as e:
                return Response({"message": PAGE_NOT_FOUND,"status":False}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(result_page, many=True)
            res_data["message"] = "Books fetch successfully"
            res_data["status"] = True
            res_data["books"] = serializer.data
            res_data["total_recors"] = queryset.count()
            res_data['page_count'] = paginator.get_page_count()
            res_data['current_page'] = paginator.get_current_page()
            return Response(res_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(f"Error occurred in BookListAPIView=={e}")
            return Response({"status":False, "message":ERROR_500},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

