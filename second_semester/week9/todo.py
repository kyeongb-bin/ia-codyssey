from typing import Dict
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

todo_list = []


@router.post('/add_todo')
def add_todo(todo_item: Dict) -> JSONResponse:
    """
    todo_list에 새로운 항목을 추가하는 함수
    POST 방식으로 동작한다.
    """
    if not todo_item:
        raise HTTPException(
            status_code=400,
            detail='빈 값은 입력할 수 없습니다.'
        )

    todo_list.append(todo_item)
    return JSONResponse(
        content={'message': 'Todo 항목이 추가되었습니다.', 'item': todo_item}
    )


@router.get('/retrieve_todo')
def retrieve_todo() -> JSONResponse:
    """
    todo_list를 가져오는 함수
    GET 방식으로 동작한다.
    """
    return JSONResponse(content={'todo_list': todo_list})


