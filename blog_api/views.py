from rest_framework import status
from rest_framework.parsers import MultiPartParser , FormParser , JSONParser , FileUploadParser
# from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializer import *
from .models import *
from .Paginatiion import *
from auth_api.models import User_profile
from auth_api.serializer import UserprofileSerializer
from rest_framework import filters
from django.http import JsonResponse
# Create your views here.

                                    # ----------------------------- #
                                    #      SEARCH POST VEIWS        #
                                    # ----------------------------- #



class post_searcheveiw(generics.ListAPIView):
    """
    create data of post model
    """
    queryset = post.objects.all()
    serializer_class = postSerializer
    pagination_class = UpgradePagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content' ]





                                    # ----------------------- #
                                    #       POST VEIWS        #
                                    # ----------------------- #



class post_listveiw(APIView ,UpgradePagination):
    """
    list veiw of post model
    """
    parser_classes = (MultiPartParser,FormParser,JSONParser ,FileUploadParser)
    def get(self, request, *args, **kwargs):
        posts_list = post.objects.filter(status="PUBLISHED").all()
        posts = self.paginate_queryset(posts_list, request, view=self)
        serializer = postSerializer(posts,many = True)
        return self.get_paginated_response(serializer.data)



class post_createveiw(APIView):
    """
    create data of post model
    """
    parser_classes = (MultiPartParser,FormParser )
    permission_class = [IsAuthenticated,]
    def post(self, request, format=None):
        serializer = postSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class post_detailveiw(APIView):
    """
    detail veiw and delete data of post model
    """
    def get_object(self, pk):
        try:
            return post.objects.get(pk=pk)
        except post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post_obj = self.get_object(pk)
        serializer = postSerializer(post_obj)
        return Response(serializer.data)

# ,context={'request': request}

class post_updatedeleteveiw(APIView):
    """
    update data and delete data of post model.
    """
    permission_class = [IsAuthenticated,]
    def get_object(self, pk):
        try:
            return post.objects.get(pk=pk)
        except post.DoesNotExist:
            raise Http404
    
    def put(self, request, pk, format=None):
        post_obj = self.get_object(pk)
        if post_obj.author == request.user:
            serializer = postSerializer(post_obj, data=request.data , context={'request': request})
            if serializer.is_valid():
                serializer.save(update_fields=['id' , 'author' , 'title' , 'categories' , 'excerpt' , 'status' , 'content'])
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'response':"You did not have a permission"
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        # print(request)
        post_obj = self.get_object(pk)
        if post_obj.author == request.user:
            post_obj.delete()
            return Response(status=status.HTTP_200_OK)
        return Response({
            'response':"You did not have a permission"
        }, status=status.HTTP_400_BAD_REQUEST)


                                    # ----------------------- #
                                    #  POST CATEGORIES VEIWS  #
                                    # ----------------------- #



class postcategories_listveiw(APIView):
    """
    list veiw of post model
    """
    pagination_class = UpgradePagination
    
    def get_object(self, catagorizer):
        try:
            return post.objects.all().filter(categories=catagorizer)
        except post.DoesNotExist:
            raise Http404


    def get(self, request, catagorizer, format=None):
        print(request)
        post_obj = self.get_object(catagorizer)
        serializer = postSerializer(post_obj , many=True)
        return Response(serializer.data)



                                    # ----------------------- #
                                    #    POST STATUS VEIWS    #
                                    # ----------------------- #



class poststatus_listveiw(APIView):
    """
    list veiw of post model
    """
    def get_object(self, state):
        try:
            return post.objects.all().filter(status=state)
        except post.DoesNotExist:
            raise Http404


    def get(self, request, state, format=None):
        post_obj = self.get_object(state)
        serializer = postSerializer(post_obj , many=True)
        return Response(serializer.data)



                                    # ----------------------- #
                                    #  POST ACHIVEMENT VEIWS  #
                                    # ----------------------- #



# class postAchivements_listveiw(generics.ListAPIView):
#     queryset = postAchivements.objects.all()
#     serializer_class = postachivementSerializer


class postAchivements_detailveiw(APIView):
    """
    Retrieve a post_obj instance.
    """
    def get_object(self, pk):
        try:
            return postAchivements.objects.get(pk=pk)
        except postAchivements.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post_obj = self.get_object(pk)
        serializer = postachivementSerializer(post_obj)
        return Response(serializer.data)


class postAchivements_updateveiw(APIView):
    """
    update data of post model.
    """
    permission_class = [IsAuthenticated,]
    def get_object(self, pk):
        try:
            return postAchivements.objects.get(pk=pk)
        except postAchivements.DoesNotExist:
            raise Http404
    
    def put(self, request, pk, format=None):
        post_obj = self.get_object(pk)
        serializer = postachivementSerializer(post_obj, data=request.data , context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



                                    # ----------------------- #
                                    #      COMMENT VEIWS      #
                                    # ----------------------- #



class comment_listveiw(APIView):
    """
    list veiw of post model
    """
    def get_object(self,postid):
        try:
            return comments.objects.filter(post_id = postid).all()
        except comments.DoesNotExist:
            raise Http404
    
    def get(self, request, postid, format=None):
        post_obj = self.get_object(postid)
        serializer = commentSerializer(post_obj ,many=True)
        return Response(serializer.data)




class comment_createveiw(APIView):
    """
    create data of post model
    """

    permission_class = [IsAuthenticated,]

    def post(self , id, request , format=None):
        comment = commentSerializer(data=request.data)
        if comment.is_valid():
            comment.save(author=self.request.user , post_id=id)
            return Response(status=status.HTTP_201_CREATED)
        return Response(data=comment.errors, status=status.HTTP_400_BAD_REQUEST)

    
        serializer_class = commentSerializer


class comment_deleteveiw(APIView):
    """
    detail veiw and delete data of comment model
    """
    permission_class = [IsAuthenticated,]
    def get_object(self, pk , postid):
        try:
            return comments.objects.get(pk = pk , post_id = postid)
        except comments.DoesNotExist:
            raise Http404


    def delete(self, request, pk , postid , format=None):
        post_obj = self.get_object(pk , postid)
        post_obj.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


                                    # --------------------------- #
                                    #      AUTHOR INFO VEIWS      #
                                    # --------------------------- #

class PostAutherInfo(APIView):
    def get_object(self, id):
        try:
            return  User.objects.get(id=id)  , User_profile.objects.filter(id=id).first() , post.objects.filter(author=id)[:4]
        except post.DoesNotExist:
            raise Http404
    
    def get(self,request,id, format=None):
        user , user_profile , userrecent_post= self.get_object(id)
        user_pro = UserprofileSerializer(user_profile)
        recentpost = postSerializer(userrecent_post,many=True)
        return Response({
            "authorName":user.username,
            "authorprofile":user_pro.data,
            "autherrecentpost":recentpost.data
        },status=status.HTTP_200_OK)
    
class UserCompleteInfo(APIView):

    def get_object(self , id):
        try:
            return User.objects.get(id=id)  , User_profile.objects.filter(id=id).first() , post.objects.filter(author=id,status="PUBLISHED") , post.objects.filter(author=id,status="DRAFT")
        except post.DoesNotExist:
            raise Http404

    def get(self , request, id , format=None):
        user_info , userprofile_info , userpost_published , userpost_draft =  self.get_object(id)

        userprofile_info = UserprofileSerializer(userprofile_info)
        userpost_published = postSerializer(userpost_published,many=True)
        userpost_draft = postSerializer(userpost_draft,many=True)
 
        return Response({
            "username": user_info.username,
            "userprofile":userprofile_info.data,
            "userpublisedpost":userpost_published.data,
            "userdraftpost":userpost_draft.data
        },status=status.HTTP_200_OK)


class usersmallInfo(APIView):
    def get_object(self, id):
        try:
            return  User.objects.get(id=id)  , User_profile.objects.filter(id=id).first() 
        except post.DoesNotExist:
            raise Http404
    
    def get(self,request,id, format=None):
        user , user_profile = self.get_object(id)
        user_pro = UserprofileSerializer(user_profile)
        
        return Response({
            "authorName":user.username,
            "authorprofile":user_pro.data,
  
        },status=status.HTTP_200_OK)