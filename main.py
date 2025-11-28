from mirror import Mirror
import os
import shutil

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("Press Enter to continue...")

def commands():
    print("Comandos:")
    print("info <username>            - Informacion del user")
    print("followers <username>       - Lista de seguidores de un usuario")
    print("following <username>       - Lista de seguidos de un usuario")
    print("mutuals <username>         - Mutuals de un usuario")
    print("notfollowed <username>     - Seguidos que no siguen de vuelta al user")
    print("notfollowing <username>    - Seguidores que el user no sigue de vuelta")
    print("exit                       - Salir")

def print_user_table(users, title=None):
    if users is None:
        return
    # compute column widths
    uname_col = max((len(u.get('Usuario') or '') for u in users), default=7)
    name_col = max((len(u.get('Nombre') or '') for u in users), default=4)
    id_col = max((len(str(u.get('ID') or '')) for u in users), default=2)

    # clamp to terminal width
    term_width = shutil.get_terminal_size((80, 20)).columns
    # minimal spacing
    spacing = 2
    # header
    header = f"{'Usuario'.ljust(uname_col)}{' ' * spacing}{'Nombre'.ljust(name_col)}{' ' * spacing}{'ID'.ljust(id_col)}"
    print(header)
    print('-' * min(len(header), term_width))

    for u in users:
        usuario = (u.get('Usuario') or '')[:uname_col]
        nombre = (u.get('Nombre') or '')[:name_col]
        uid = str(u.get('ID') or '')
        print(f"{usuario.ljust(uname_col)}{' ' * spacing}{nombre.ljust(name_col)}{' ' * spacing}{uid.rjust(id_col)}")

def main():
    ig = None
    
    # First, try to use saved session (no credentials needed yet)
    print("Checking for saved session...")
    try:
        # Create Mirror with dummy credentials; it will try session first
        ig = Mirror("", "")
    except Exception as e:
        # Session failed or doesn't exist; ask for real credentials
        print(f"Session loading failed: {e}\n")
        username = input("Usuario de ig: ")
        password = input("Contraseña de ig: ")
        ig = Mirror(username, password)

    while True:
        cls()
        print ("================ Mirror for Instagram ===================")
        commands()

        cmd = input("mirror> ").strip().split()

        if len(cmd) == 0:
            continue

        action = cmd[0].lower()

        # info 
        if action == "info" and len(cmd) == 2:
            target = cmd[1]
            print(f"\nInfo de {target}: \n")
            info = ig.getUserInfo(target)

            if info:
                for k, v in info.items():
                    print(f"{k}: {v}")
            
            pause()

        # followers 
        elif action == "followers" and len(cmd) == 2:
            target = cmd[1]
            print(f"\nFollowers de {target}:\n")
            followers = ig.getFollowers(target)

            if followers is not None:
                print(f"Total followers: {len(followers)}")
                print_user_table(followers)

            pause()

        # notfollowing
        elif action == "notfollowing" and len(cmd) == 2:
            target = cmd[1]
            print(f"\nSeguidores que {target} no sigue de vuelta:\n")
            not_following_back = ig.getNotFollowingBack(target)

            if not_following_back is not None:
                print(f"Total not-following-back: {len(not_following_back)}")
                print_user_table(not_following_back)

            pause()

        # mutuals
        elif action == "mutuals" and len(cmd) == 2:
            target = cmd[1]
            print(f"\nMutuals de {target}:\n")
            mutuals = ig.getMutuals(target)

            if mutuals is not None:
                print(f"Total mutuals: {len(mutuals)}")
                print_user_table(mutuals)

            pause()
        
        # notfollowed
        elif action == "notfollowed" and len(cmd) == 2:
            target = cmd[1]
            print(f"\nSeguidos que no siguen de vuelta a {target}:\n")
            not_followed = ig.getNotFollowedBack(target)

            if not_followed is not None:
                print(f"Total not-followed-back: {len(not_followed)}")
                print_user_table(not_followed)

            pause()

        elif action == "exit":
            print("Saliendo...")
            break

if __name__ == "__main__":
    main()
