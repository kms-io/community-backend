from typing import List, Type

from pydantic import BaseModel, Field, create_model


class CustomBaseModel(BaseModel):
    """
        기존 BaseModel에 custom classmethod 추가.
        all_optional : 모든 속성 타입을 Optional로 변환
        omit_fields : 기존 클래스에서 특정 field들을 제거한 클래스를 반환
    """
    @classmethod
    def all_optional(cls, name) -> Type["CustomBaseModel"]:
        return create_model(
            name,
            __base__=cls,
            **{
                name: (
                    info.annotation,
                    Field(None, title=info.title, description=info.description, examples=info.examples)
                ) for name, info in cls.model_fields.items()
            }
        )

    @classmethod
    def omit_fields(cls, name: str, attrs: List[str]) -> Type["CustomBaseModel"]:
        new_annotations = {
            name: (
                info.annotation,
                Field(info.default, title=info.title, description=info.description, examples=info.examples)
            ) for name, info in cls.model_fields.items() if name not in attrs
        }
        return create_model(name, __base__=CustomBaseModel, **new_annotations)
