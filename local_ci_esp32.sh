#! /usr/bin/bash


LOCAL_CI_PATH="tools/local_ci"
ESP32_FLASH="True"
ESP32_TEST="True"
ESP32_TEST_BOARD="esp32"

TOP_MPY_DIR=$PWD

ESP32_BOARD="ESP32_GENERIC"
ESP32_BOARD_DIR=$TOP_MPY_DIR/ports/esp32/boards

echo "PORT: esp32 CI"
source tools/ci.sh
source .env


# ports/esp32

# GitHub tag of ESP-IDF to use for CI (note: must be a tag or a branch)
IDF_VER=v5.0.4

export IDF_CCACHE_ENABLE=1

function ci_esp32_idf_setup {
    pip3 install pyelftools
    git clone --depth 1 --branch $IDF_VER https://github.com/espressif/esp-idf.git
    # doing a treeless clone isn't quite as good as --shallow-submodules, but it
    # is smaller than full clones and works when the submodule commit isn't a head.
    git -C esp-idf submodule update --init --recursive --filter=tree:0
    # GIT_DIR="${PWD}/esp-idf/.git" esp-idf/install.sh
}

function ci_esp32_prebuild_remote {
    # source esp-idf/export.sh
    make ${MAKEOPTS} -C mpy-cross
    SUBMODULES="lib/berkeley-db-1.xx lib/micropython-lib"

    git submodule sync $SUBMODULES
    git submodule update --init $SUBMODULES

}
export IDF_PATH="$PWD/esp-idf"
export PATH="$IDF_PATH/tools:${PATH}"
# echo $PATH
# GIT_WORK_TREE="$PWD/esp-idf" 

# TODO: check if esp-idf exists.
#
# ci_esp32_idf_setup # uncomment if there is no idf setup yet
GIT_DIR="${PWD}/esp-idf/.git" esp-idf/install.sh
GIT_DIR="${PWD}/esp-idf/.git" . esp-idf/export.sh
# Pin IDF_VERSION
GIT_DIR="${PWD}/esp-idf/.git" git describe > $IDF_PATH/version.txt
echo "IDF_PATH:" $IDF_PATH

# idf_tools.py list
#

# BUILD

#TODO: parallelise building different boards

ci_esp32_prebuild_remote

# TODO: multiple boards
# if $<PORT>_BOARD_RUNNER
# call board_runner.py --> allow build multiple boards and multiprocessing

$LOCAL_CI_PATH/board_runner.py esp32 
#
#else: run this
#

exit $?

# make clean -C ports/esp32  BOARD_DIR=$ESP32_BOARD_DIR/$ESP32_BOARD
# make -C ports/esp32  BOARD_DIR=$ESP32_BOARD_DIR/$ESP32_BOARD -j16


# if [ $? -eq 0 ];
# then
#   echo "PORT: esp32 BUILD: [ OK ]"
# else
#   echo "PORT: esp32 BUILD: [ FAILED ]" >&2 # STDERR
#   exit 1
# fi

# # FLASH
# if test "$ESP32_FLASH" == "True";
#     then
#         echo "Flashing firmware"
#         make -C ports/esp32 BOARD_DIR=$ESP32_BOARD_DIR/$ESP32_BOARD PORT=$ESP32_DEVICE deploy 

#         flash_result=$?

#         if [ $flash_result -eq 0 ];
#         then
#           echo "PORT: esp32 FIRMWARE FLASH: [ OK ]"
#         else
#           echo "PORT: esp32 FIRMWARE FLASH: [ FAILED ]" >&2 # STDERR
#           exit 1
#         fi

#         sleep 3
# else 
#     echo "PORT: esp32 flashing SKIP"
# fi

# echo "Running tests..."
# $LOCAL_CI_PATH/device_test_runner.py $ESP32_TEST_BOARD

# test_result=$?

# if [ $test_result -eq 0 ];
# then
#   echo "PORT: esp32 TESTS: [ OK ]"
# else
#   echo "PORT: esp32 TESTS: [ FAILED ]" >&2 # STDERR
#   # exit 1
# fi


# # CI RESULT
# if [ $test_result -eq 0 ];
# then
#     :
# else 
#     exit 1 
# fi 
