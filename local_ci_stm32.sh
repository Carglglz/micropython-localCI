#! /usr/bin/bash


LOCAL_CI_PATH="../micropython-localCI"
STM32_TEST="True"
STM32_FLASH="True"
STM32_BOARD="PYBV11"
STM32_TEST_BOARD="stm32" # mapped to pyboard in device_test_runner.py
STM32_BOARD_DIR=$PWD/ports/stm32/boards

OK="[\u001b[32;1m OK \u001b[0m]"
FAIL="[\u001b[31;1m FAILED \u001b[0m]"
SKIP="[\u001b[33;1m SKIP\u001b[0m ]"

echo -e "PORT: stm32 CI [\u001b[32;1m RUNNING \u001b[0m]"
source tools/ci.sh
source .env 

# ports/stm32
function ci_stm32_pyb_prebuild {
    # make ${MAKEOPTS} -C mpy-cross
    SUBMODULES="lib/libhydrogen lib/stm32lib lib/micropython-lib"

    git submodule sync $SUBMODULES
    git submodule update --init $SUBMODULES

}

function ci_stm32_pyb_build {

    make -C ports/stm32 clean BOARD_DIR=$STM32_BOARD_DIR/$STM32_BOARD
    make ${MAKEOPTS} -C ports/stm32 BOARD_DIR=$STM32_BOARD_DIR/$STM32_BOARD -j8
    
}


# BUILD
ci_stm32_pyb_prebuild


# Multiple boards
if test "$STM32_BOARD_RUNNER" == "True";
    then
        echo "MODE: [ Board Runner ]"
        $LOCAL_CI_PATH/board_runner.py stm32 
        exit $?
else
    echo "MODE: [ Single Board ]"
fi


# Single board

ci_stm32_pyb_build

if [ $? -eq 0 ];
then
  echo -e "PORT: stm32 BUILD: $OK"
else
  echo -e "PORT: stm32 BUILD: $FAIL" >&2
  exit 1
fi

# FLASH
if test "$STM32_FLASH" == "True";
    then
        echo "Flashing firmware..."
        # TODO: set PORT=$STM32_DEVICE?
        tools/mpremote/mpremote.py bootloader
        sleep 2
        make -C ports/stm32 BOARD_DIR=$STM32_BOARD_DIR/$STM32_BOARD deploy 
        flash_result=$?

        if [ $flash_result -eq 0 ];
        then
          echo -e "PORT: stm32 FIRMWARE FLASH: $OK"
        else
          echo -e "PORT: stm32 FIRMWARE FLASH: $FAIL" >&2
          exit 1
        fi

        sleep 3
else 
    echo -e "PORT: stm32 flashing $SKIP"
fi

# TEST:

echo "Running tests..."
$LOCAL_CI_PATH/device_test_runner.py $STM32_TEST_BOARD

test_result=$?

if [ $test_result -eq 0 ];
then
  echo -e "PORT: stm32 TESTS: $OK"
else
  echo -e "PORT: stm32 TESTS: $FAIL" >&2
  # exit 1
fi


# CI RESULT
if [ $test_result -eq 0 ];
then
    :
else 
    exit 1 
fi 
