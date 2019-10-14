# generic

from django.db.models import Q
from rest_framework import generics, mixins

from postings.models import UserProfile
from .permissions import IsOwnerOrReadOnly
from .serializers import UserProfileSerializer


class UserProfileAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field            = 'pk' 
    serializer_class        = UserProfileSerializer
    #queryset                = UserProfile.objects.all()

    def get_queryset(self):
        qs = UserProfile.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                    Q(name__icontains=query)|
                    Q(address__icontains=query)|
                    Q(city__icontains=query)|
                    Q(contact__icontains=query)
                    ).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class UserProfileRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field            = 'pk'
    serializer_class        = UserProfileSerializer
    permission_classes      = [IsOwnerOrReadOnly]
    #queryset                = UserProfile.objects.all()

    def get_queryset(self):
        return UserProfile.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return UserProfile.objects.get(pk=pk)
