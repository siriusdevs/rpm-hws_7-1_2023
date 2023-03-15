"""User entrypoints."""
import glob
import os
from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException, UploadFile, Depends
from fastapi.responses import FileResponse

from config import SQL_INSERT_USER_IMAGE, SQL_UPDATE_IMAGE, SQL_SELECT_USER_IMAGE, FILES_DIR, SQL_DELETE
from http_config import HTTP_CREATE, HTTP_NOT_FOUND, HTTP_FORBIDDEN, HTTP_GONE
from src.database import is_this_user, db_cursor, db_connection, check_token
from .schemas import Image, UserImage, ModelImageUser

router = APIRouter(
    prefix="/image/user",
    tags=["User Image"]
)


@router.post("/{user_name}/", status_code=HTTP_CREATE)
def create_user_image(token: str, upload_file: UploadFile, user_name: str, image: Image = Depends()):
    """Creates new user image.

    Args:
        token (str): for auth user.
        image (Image): title, explanation and date of new image.
        user_name (str): photo owner name.
        upload_file (UploadFile): image in bytes.

    Raises:
        HTTPException: Forbidden if wrong token.
    """
    if not is_this_user(token, user_name):
        raise HTTPException(status_code=HTTP_FORBIDDEN, detail="Wrong token")
    db_cursor.execute("select * from token")
    db_cursor.execute(SQL_INSERT_USER_IMAGE, (user_name, image.title, image.explanation, image.date))
    db_connection.commit()
    image_id = db_cursor.fetchone().get("id")
    request = f"url = '/{user_name}/{image_id}/data'"
    db_cursor.execute(SQL_UPDATE_IMAGE.format(request=request, parameters="where id = %s"), (image_id,))
    db_connection.commit()
    if not os.path.isdir(FILES_DIR.format(user="", file_name="")[:-1]):
        os.mkdir(FILES_DIR.format(user="", file_name="")[:-1])
    suffix = Path(upload_file.filename).suffix
    path = FILES_DIR.format(user=user_name, file_name=f"{image_id}{suffix}")
    if not os.path.isdir(FILES_DIR.format(user=user_name, file_name="")):
        os.mkdir(FILES_DIR.format(user=user_name, file_name=""))
    with open(path, "wb+") as fi:
        fi.write(upload_file.file.read())
    db_cursor.execute(SQL_SELECT_USER_IMAGE.format(request="*", parameters="where id = %s"), (image_id,))
    return db_cursor.fetchone()


@router.get("/{user_name}/", response_model=List[UserImage])
def user_images(token: str, user_name: str):
    """Returns all user's images.

    Args:
        token (str): for auth user.
        user_name (str): photo owner name.

    Raises:
        HTTPException: Forbidden if wrong token. Not found if not exist.
    """
    if not check_token(token):
        raise HTTPException(status_code=HTTP_FORBIDDEN, detail="Wrong token")
    db_cursor.execute(SQL_SELECT_USER_IMAGE.format(request="*", parameters="where user_name = %s"), (user_name,))
    response = db_cursor.fetchall()
    if not response:
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail=f"User '{user_name}' not found")
    return response


@router.put("/{user_name}/{image_id}/", status_code=HTTP_CREATE, description="Update user image")
def update_user_image(token: str, image_id: int, upload_file: UploadFile, user_name: str, image: Image = Depends()):
    """Updates a user's image.

    Args:
        token (str): for auth user.
        image_id (int): photo's number.
        upload_file (UploadFile):  image in bytes.
        user_name (str): photo owner name.
        image (Image): title, explanation and date for update image.

    Raises:
        HTTPException: Forbidden if wrong token. Not found if not exist.
    """
    if not is_this_user(token, user_name):
        raise HTTPException(status_code=HTTP_FORBIDDEN, detail="Wrong token or you can't edit it")
    db_cursor.execute(SQL_SELECT_USER_IMAGE.format(request="*", parameters="where id = %s"), (image_id,))
    if not db_cursor.fetchone():
        return HTTPException(status_code=HTTP_NOT_FOUND, detail="Not found")
    for key, image_value in image.dict().items():
        db_cursor.execute(SQL_UPDATE_IMAGE.format(request=f"{key} = %s", parameters="where id = %s"),
                          (image_value, image_id))
    db_connection.commit()
    suffix = Path(upload_file.filename).suffix
    if not os.path.isdir(FILES_DIR.format(user="", file_name="")[:-1]):
        os.mkdir(FILES_DIR.format(user="", file_name="")[:-1])
    if not os.path.isdir(FILES_DIR.format(user=user_name, file_name="")):
        os.mkdir(FILES_DIR.format(user=user_name, file_name=""))
    with open(FILES_DIR.format(user=user_name, file_name=f"{image_id}{suffix}"), "wb+") as fi:
        fi.write(upload_file.file.read())
    db_cursor.execute(SQL_SELECT_USER_IMAGE.format(request="*", parameters="where id = %s"), (image_id,))
    return db_cursor.fetchone()


@router.delete("/{user_name}/{image_id}/")
def delete_user_image(token: str, image_id: int, user_name: str):
    """Deletes a user's image.

    Args:
        token (str): for auth user.
        image_id (int): photo's number.
        user_name (str): photo owner name.

    Raises:
        HTTPException: Forbidden if wrong token. Not found if not exist.
    """
    if not is_this_user(token, user_name):
        raise HTTPException(status_code=HTTP_FORBIDDEN, detail="Wrong token or you can't edit it")
    db_cursor.execute(SQL_SELECT_USER_IMAGE.format(request="*", parameters="where id = %s"), (image_id,))
    img = db_cursor.fetchone()
    if not img:
        return HTTPException(status_code=HTTP_NOT_FOUND, detail="Not found")
    db_cursor.execute(SQL_DELETE.format(parameters=f"where id = {image_id}"))
    db_connection.commit()
    file_names = glob.glob(root_dir=FILES_DIR.format(user=user_name, file_name=""), pathname=f"{image_id}.*")
    if file_names:
        os.remove(FILES_DIR.format(user=user_name, file_name=file_names[0]))
    return {"detail": "successfully delete"}


@router.get("/{user_name}/{image_id}/{model_user}")
@router.get("/{user_name}/{image_id}/", response_model=UserImage)
def user_image(token: str, user_name: str, image_id: int, model_user: ModelImageUser = None):
    """Returns a user's image.

    Args:
        token (str): for auth user.
        image_id (int): photo's number.
        user_name (str): photo owner name.
        model_user (ModelImageUser): allowed path.

    Raises:
        HTTPException: Forbidden if wrong token. Not found if not exist. Gone if file was deleted.
    """
    if not check_token(token):
        raise HTTPException(status_code=HTTP_FORBIDDEN, detail="Wrong token")
    if not model_user:
        db_cursor.execute(SQL_SELECT_USER_IMAGE.format(request="*", parameters=f"where id = {image_id}"))
        return db_cursor.fetchone()

    if model_user is ModelImageUser.data:
        file_names = glob.glob(root_dir=FILES_DIR.format(user=user_name, file_name=""), pathname=f"{image_id}.*")
        if not file_names:
            return HTTPException(status_code=HTTP_GONE, detail="File was deleted")
        path = Path(FILES_DIR.format(user=user_name, file_name=file_names[0]))
        if not path.is_file():
            return HTTPException(status_code=HTTP_GONE, detail="File was deleted")
        return FileResponse(path)

    db_cursor.execute(SQL_SELECT_USER_IMAGE.format(request=model_user.value, parameters=f"where id = {image_id}"))
    image = db_cursor.fetchone()
    return image if image else HTTPException(status_code=HTTP_NOT_FOUND, detail="Not found")
