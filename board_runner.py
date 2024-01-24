# sys.argv.pop() --> port

# os.getenv <PORT>_BOARDS = "<port>_boards.yaml"
# default options
# <PORT>_BUILD
# <PORT>_FLASH
# <PORT>_TEST
# os.getenv <PORT>_BOARD_DIR = "$ASYNCMDBOARS"

# <port>_boards.yaml
# boards:
#   PYBV11:
#       BOARD_DIR: "boards"
#       BUILD: true
#       FLASH: true
#       TEST: true
#
#       CUSTOM_TESTS: ''/ false
#       PORT: "/dev/ttyACM0"


# def build_board(port, board_dir, board):

# def flash_board(port, board_dir, board):

# def test_board(port, board_dir, board):


# def board_runner(port, board_dir, board):

# build_board

# flash_board

# test_board
# parallel redirect output


# os.getenv(BUILD_BOARDS_PARALLEL)

# serial
# for boards in BOARDS
# parallel:
# boards_args = [(port, board_dir, board) for board in BOARDS]
# with Pool(len(boards)) as p:

# p.map(build_boards, board_args)
