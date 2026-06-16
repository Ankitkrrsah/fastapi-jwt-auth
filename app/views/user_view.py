from fastapi import APIRouter, HTTPException, Depends
import psycopg2
from app.models.user_model import UserInput, UserResponse, UserLogin, RefreshTokenRequest
from app.presenters.auth_presenter import (
    hash_password, verify_password, create_access_token, 
    create_refresh_token, verify_token, verify_refresh_token
)
from app.db.database import get_db
from datetime import datetime, timedelta, timezone

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserInput, db=Depends(get_db)):
    cur, conn = db
    try:
        hashed_password = hash_password(user.password)
        cur.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
            """,
            (user.name, user.email, hashed_password)
        )
        conn.commit()
        return UserResponse(name=user.name, email=user.email)

    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")

    except Exception:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/login")
def login(user: UserLogin, db=Depends(get_db)):
    cur, conn = db

    cur.execute(
        """
        SELECT id, name, email, password
        FROM users
        WHERE email = %s
        """,
        (user.email,)
    )
    result = cur.fetchone()

    if not result or not verify_password(user.password, result[3]):
        raise HTTPException(status_code=401, detail="Either email or password is incorrect")

    user_id = result[0]
    email = result[2]

    access_token = create_access_token({
        "sub": str(user_id),
        "email": email
    })

    refresh_token = create_refresh_token({
        "sub": str(user_id),
        "email": email
    })

    refresh_expiry = datetime.now(timezone.utc) + timedelta(days=7)

    cur.execute(
        """
        INSERT INTO refresh_tokens (user_id, token, expires_at)
        VALUES (%s, %s, %s)
        """,
        (user_id, refresh_token, refresh_expiry)
    )
    conn.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def genNewToken(data: RefreshTokenRequest, db=Depends(get_db)):
    cur, conn = db

    payload = verify_refresh_token(data.refresh_token)

    cur.execute(
        """
        SELECT user_id FROM refresh_tokens
        WHERE token = %s
        """,
        (data.refresh_token,)
    )
    result = cur.fetchone()

    if not result:
        raise HTTPException(status_code=401, detail="Refresh token revoked")

    cur.execute(
        """
        DELETE FROM refresh_tokens
        WHERE token = %s
        """,
        (data.refresh_token,)
    )

    new_refresh_token = create_refresh_token({
        "sub": payload["sub"],
        "email": payload["email"]
    })

    new_refresh_expiry = datetime.now(timezone.utc) + timedelta(days=7)

    cur.execute(
        """
        INSERT INTO refresh_tokens (user_id, token, expires_at)
        VALUES (%s, %s, %s)
        """,
        (result[0], new_refresh_token, new_refresh_expiry)
    )
    conn.commit()

    new_access_token = create_access_token({
        "sub": payload["sub"],
        "email": payload["email"]
    })

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(data: RefreshTokenRequest, db=Depends(get_db), user=Depends(verify_token)):
    cur, conn = db

    cur.execute(
        """
        DELETE FROM refresh_tokens
        WHERE token = %s
        """,
        (data.refresh_token,)
    )
    conn.commit()

    if cur.rowcount == 0:
        raise HTTPException(status_code=400, detail="Invalid refresh token")

    return {"message": "Successfully logged out"}

@router.get("/home")
def home(user=Depends(verify_token)):
    return {
        "message": f"Welcome {user['email']}",
        "user": user
    }
