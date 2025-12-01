from instagrapi import Client
from instagrapi.exceptions import (
    BadPassword, LoginRequired, ChallengeRequired,
    FeedbackRequired, PleaseWaitFewMinutes
)
import contextlib
import os
import logging
import json

logger = logging.getLogger(__name__)

# Suppress all library loggers completely to prevent HTTP request logs
for logger_name in ['instagrapi', 'urllib3', 'urllib3.connectionpool', 'requests', 'httpx', 'asyncio']:
    logging.getLogger(logger_name).setLevel(logging.ERROR)
    logging.getLogger(logger_name).propagate = False

# Suppress instagrapi library logging (info/debug/error messages that clutter output)
logging.getLogger('instagrapi').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('urllib3.connectionpool').setLevel(logging.CRITICAL)
logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('httpx').setLevel(logging.CRITICAL)
logging.getLogger('asyncio').setLevel(logging.CRITICAL)

class Mirror:

    def __init__(self, username, password, session_file="session.json"):
        print("Iniciando sesion en Instagram...")

        self.session_file = session_file
        self.username = username
        self.password = password

        self.api = Client()

        # Attempt to login with session persistence (try session first, no credentials needed)
        self.loginUser()
        print(f"Sesion iniciada como {self.username}\n")

    def loginUser(self):
        """Login with session persistence and validation."""
        login_via_session = False

        # Try to load and use saved session FIRST (no credentials needed)
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    session = json.load(f)
                    self.api.set_settings(session)
                    logger.info(f"Loaded session from {self.session_file}")
                    print("Session file found. Validating saved session...")

                    # Validate session by attempting an API call
                    try:
                        self.api.get_timeline_feed()
                        logger.info("Session is valid")
                        print("✓ Session is valid. Using saved session.")
                        login_via_session = True
                        return  # Success, exit early
                    except LoginRequired:
                        logger.info("Session is invalid or expired")
                        print("✗ Session expired or invalid.")
                    except Exception as e:
                        logger.warning(f"Session validation failed: {e}")
                        print(f"✗ Session validation failed: {e}")
            except Exception as e:
                logger.warning(f"Could not load session file: {e}")
                print(f"Could not load session file: {e}")

        # If session didn't work, try password login (requires credentials)
        if not self.username or not self.password:
            raise Exception("No saved session found and no credentials provided. Please run again with credentials.")
        
        if not login_via_session:
            try:
                print("Attempting login with provided credentials...")
                self.api.login(self.username, self.password)
                self.saveSession()
                logger.info("Login successful with username/password")
                print("Login successful. Session saved.")
            except Exception as e:
                logger.error(f"Could not login with username/password: {e}")
                self.handleException(e)
                raise

    def saveSession(self):
        """Save the current session to a JSON file."""
        try:
            session = self.api.get_settings()
            with open(self.session_file, 'w') as f:
                json.dump(session, f, indent=4)
            logger.info(f"Session saved to {self.session_file}")
        except Exception as e:
            logger.warning(f"Could not save session: {e}")

    def handleException(self, exception):
        """Handle instagrapi exceptions with user-friendly messages."""
        if isinstance(exception, BadPassword):
            print("❌ Contraseña incorrecta. Verifica tus credenciales.")
            return False
        elif isinstance(exception, LoginRequired):
            print("❌ Sesion expirada. Debes volver a iniciar sesion.")
            return False
        elif isinstance(exception, ChallengeRequired):
            print("❌ Instagram requiere verificacion adicional. Intenta de nuevo mas tarde.")
            return False
        elif isinstance(exception, FeedbackRequired):
            print("❌ Instagram ha bloqueado esta accion temporalmente. Espera un tiempo antes de reintentar.")
            return False
        elif isinstance(exception, PleaseWaitFewMinutes):
            print("❌ Rate limit alcanzado. Espera unos minutos antes de reintentar.")
            return False
        else:
            print(f"❌ Error: {type(exception).__name__}: {str(exception)}")
            return False

    # =============================
    # Get IG User ID from username
    # =============================
    def getUserID(self, username):
        try:
            # suppress library-printed tracebacks that appear on stderr
            with open(os.devnull, 'w') as devnull:
                with contextlib.redirect_stderr(devnull):
                    return self.api.user_id_from_username(username)
        except Exception as e:
            logger.error(f"Error getting user ID for {username}: {e}")
            self.handleException(e)
            return None

    # =============================
    # Get user profile information
    # =============================
    def getUserInfo(self, username):
        try:
            uid = self.getUserID(username)
            if uid is None:
                return None

            # suppress library-printed tracebacks and stderr during user_info call
            with open(os.devnull, 'w') as devnull:
                with contextlib.redirect_stderr(devnull):
                    user = self.api.user_info(uid)

            return {
                "ID": user.pk,
                "Usuario": user.username,
                "Nombre": user.full_name,
                "Bio": user.biography,
                "Followers": user.follower_count,
                "Following": user.following_count,
                "Privado": user.is_private,
                "Verificado": user.is_verified,
                "Foto de perfil": user.profile_pic_url
            }

        except Exception as e:
            self.handleException(e)
            return None

    # =============================
    # Get following list
    # =============================
    def getFollowing(self, username):
        try:
            uid = self.getUserID(username)
            if uid is None:
                return None

            following = self.api.user_following(uid)

            lista = [
                {
                    "ID": u.pk,
                    "Usuario": u.username,
                    "Nombre": u.full_name,
                    "Foto de perfil": u.profile_pic_url
                }
                for u in following.values()
            ]

            return lista

        except Exception as e:
            self.handleException(e)
            return None

    # =============================
    # Get followers list
    # =============================
    def getFollowers(self, username):
        try:
            uid = self.getUserID(username)
            if uid is None:
                return None

            followers = self.api.user_followers(uid)

            lista = [
                {
                    "ID": u.pk,
                    "Usuario": u.username,
                    "Nombre": u.full_name,
                    "Foto de perfil": u.profile_pic_url
                }
                for u in followers.values()
            ]

            return lista

        except Exception as e:
            self.handleException(e)
            return None

    # =============================
    # Get mutuals list (accounts that both follow and are followed by the target)
    # =============================
    def getMutuals(self, username):
        try:
            followers = self.getFollowers(username)
            following = self.getFollowing(username)

            if followers is None or following is None:
                return None

            # Build lookups by ID (fallback to username if ID missing)
            followers_map = {}
            for u in followers:
                key = str(u.get("ID") or u.get("Usuario") or "")
                followers_map[key] = u

            following_map = {}
            for u in following:
                key = str(u.get("ID") or u.get("Usuario") or "")
                following_map[key] = u

            mutual_keys = set(followers_map.keys()) & set(following_map.keys())

            mutuals = [followers_map[k] for k in mutual_keys]
            mutuals.sort(key=lambda x: x.get("Usuario", "").lower())
            return mutuals

        except Exception as e:
            self.handleException(e)
            return None

    # =============================
    # Get accounts the target follows that do NOT follow back
    # =============================
    def getNotFollowedBack(self, username):
        try:
            followers = self.getFollowers(username)
            following = self.getFollowing(username)

            if followers is None or following is None:
                return None

            followers_keys = set()
            for u in followers:
                key = str(u.get("ID") or u.get("Usuario") or "")
                followers_keys.add(key)

            not_followed = []
            for u in following:
                key = str(u.get("ID") or u.get("Usuario") or "")
                if key not in followers_keys:
                    not_followed.append(u)

            not_followed.sort(key=lambda x: x.get("Usuario", "").lower())
            return not_followed

        except Exception as e:
            self.handleException(e)
            return None

    # =============================
    # Get accounts that follow the target but the target does NOT follow back
    # =============================
    def getNotFollowingBack(self, username):
        try:
            followers = self.getFollowers(username)
            following = self.getFollowing(username)

            if followers is None or following is None:
                return None

            following_keys = set()
            for u in following:
                key = str(u.get("ID") or u.get("Usuario") or "")
                following_keys.add(key)

            not_following_back = []
            for u in followers:
                key = str(u.get("ID") or u.get("Usuario") or "")
                if key not in following_keys:
                    not_following_back.append(u)

            not_following_back.sort(key=lambda x: x.get("Usuario", "").lower())
            return not_following_back

        except Exception as e:
            self.handleException(e)
            return None
