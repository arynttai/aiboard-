from posts.schemas import CreatePostRequest, EditPostRequest
from fastapi import HTTPException, APIRouter
import time
import os
import requests
from posts import service

router = APIRouter()


@router.get('')
async def get_posts():
    return await service.get_posts()


@router.post('')
async def create_post(post: CreatePostRequest):
    return await service.create_post(post)


@router.get('/{id}')
async def get_post(id: int):
    return await service.get_post_by_id(id)


@router.put('/{id}')
async def edit_post(id: int, post_data: EditPostRequest):
    return await service.edit_post(id, post_data)


@router.delete('/{id}')
async def delete_post(id: int):
    await service.delete_post(id)

    return {"message": "ok, deleted"}
