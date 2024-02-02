### Setup a local MicroPython CI runner 

* Automate CI builds/tests runs in the local computer or a local/private server (accessed using SSH) 
* Control which ports are built using a dotenv file and config yaml files to define which board/s are built/flashed/tested.

* Add custom hardware tests and callbacks on success/error per board.

Clone this repo and install with `$ ./install.sh` and go to 5) or do it manually

#### 1) Clone MicroPython repo 

```
$ git clone https://github.com/micropython/micropython.git micropython_CI
```
#### 2) Set this repo as a git-server-repo

```
$ cd micropython_CI/.git
$ git --bare update-server-info
$ cd ..

```
#### 3) Config git repo to allow receive operations 

```
$ git config --local receive.denyCurrentBranch ignore 
```

or add this to `.git/config` 

```
[receive]
        denyCurrentBranch = ignore
```

#### 4) Setup git hooks

Copy git hooks from `./git_hooks` into `../micropython_CI/.git/hooks`

```
$ cp ./git_hooks/post-*  ../micropython_CI/.git/hooks/
```

#### 5) Add micropython CI repo as remote

In your MicroPython development repo add the MicroPython CI repo as a remote

.e.g 
```
$ git remote add localci ssh://myserver.local/<PATH_TO_CI_REPO>/micropython_CI/.git

```

#### 6) Push commits to CI repo 

Create a new branch, make some changes, commit and then pust to this CI repo e.g. pushing a `test_ci` branch with some changes:

```
$ git push -f localci test_ci
Enumerating objects: 13, done.
Counting objects: 100% (13/13), done.
Delta compression using up to 4 threads
Compressing objects: 100% (11/11), done.
Writing objects: 100% (11/11), 2.25 KiB | 1.13 MiB/s, done.
Total 11 (delta 3), reused 0 (delta 0), pack-reused 0
remote: stashing local changes...
remote: GIT_WORK_TREE:  /mnt/ssd/LOCAL_CI/micropython_CI
remote: GIT_DIR
remote: /mnt/ssd/LOCAL_CI/micropython_CI/.git
remote: No local changes to save
remote: checking out files...
remote: BRANCH:  test_ci
remote: TAG:  v1.23.0-preview-48-ga4ff3d733
remote: updating remote...
remote: done.
remote: GIT DIR:  /mnt/ssd/LOCAL_CI/micropython_CI/.git
remote: UPDATED PATHS:
remote: tools/local_ci/README.md
remote: tools/local_ci/ci_runner.py
remote: tools/local_ci/git_hooks/post-receive
remote: tools/local_ci/git_hooks/post-update
remote: tools/local_ci/local_ci_stm32.sh
remote: tools/local_ci/local_ci_unix.sh
remote:
remote: Nothing to build/test
To ssh://myserver.local/mnt/ssd/LOCAL_CI/micropython_CI/.git
 + 344f67167...a4ff3d733 test_ci -> test_ci (forced update)

```

The CI runner will detect updated paths and run the appropriate port CI runners. e.g. unix port

```
$ git push -f localci mbedtls3 
Enumerating objects: 103, done.
Counting objects: 100% (103/103), done.
Delta compression using up to 4 threads
Compressing objects: 100% (58/58), done.
Writing objects: 100% (59/59), 10.46 KiB | 1.31 MiB/s, done.
Total 59 (delta 47), reused 0 (delta 0), pack-reused 0
remote: stashing local changes...
remote: GIT_WORK_TREE:  /mnt/ssd/LOCAL_CI/micropython_CI
remote: GIT_DIR
remote: /mnt/ssd/LOCAL_CI/micropython_CI/.git
remote: No local changes to save
remote: checking out files...
remote: BRANCH:  mbedtls3
remote: TAG:  v1.23.0-preview-37-gc4f384221
remote: updating remote...
remote: done.
remote: GIT DIR:  /mnt/ssd/LOCAL_CI/micropython_CI/.git
remote: PORT: unix CI
remote: make: Entering directory '/mnt/ssd/LOCAL_CI/micropython_CI/ports/unix'
remote: Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
remote: rm -f build-standard/micropython
remote: rm -f build-standard/micropython.map
remote: rm -rf build-standard
remote: make: Leaving directory '/mnt/ssd/LOCAL_CI/micropython_CI/ports/unix'
remote: make: Entering directory '/mnt/ssd/LOCAL_CI/micropython_CI/mpy-cross'
remote: Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
remote: GEN build/genhdr/mpversion.h
remote: CC ../py/modsys.c
remote: CC main.c
remote: LINK build/mpy-cross
remote:    text    data     bss     dec     hex filename
remote:  322495   13776     856  337127   524e7 build/mpy-cross
remote: make: Leaving directory '/mnt/ssd/LOCAL_CI/micropython_CI/mpy-cross'
remote: Synchronizing submodule url for 'lib/berkeley-db-1.xx'
remote: Synchronizing submodule url for 'lib/mbedtls'
remote: Synchronizing submodule url for 'lib/micropython-lib'
remote: make: Entering directory '/mnt/ssd/LOCAL_CI/micropython_CI/ports/unix'
remote: Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
remote: make: Nothing to be done for 'deplibs'.
remote: make: Leaving directory '/mnt/ssd/LOCAL_CI/micropython_CI/ports/unix'
remote: make: Entering directory '/mnt/ssd/LOCAL_CI/micropython_CI/ports/unix'
remote: Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
remote: mkdir -p build-standard/genhdr
remote: mkdir -p build-standard/build-standard/
remote: mkdir -p build-standard/extmod/
remote: mkdir -p build-standard/lib/berkeley-db-1.xx/btree/
remote: mkdir -p build-standard/lib/berkeley-db-1.xx/mpool/
remote: mkdir -p build-standard/lib/littlefs/
remote: mkdir -p build-standard/lib/mbedtls/library/
remote: mkdir -p build-standard/lib/mbedtls_errors/
remote: mkdir -p build-standard/lib/oofatfs/
remote: mkdir -p build-standard/py/
remote: mkdir -p build-standard/shared/libc/
remote: mkdir -p build-standard/shared/readline/
remote: mkdir -p build-standard/shared/runtime/
remote: mkdir -p build-standard/shared/timeutils/
remote: GEN build-standard/genhdr/mpversion.h
remote: GEN build-standard/genhdr/qstr.i.last
remote: GEN build-standard/genhdr/qstr.split
remote: GEN build-standard/genhdr/moduledefs.split
remote: GEN build-standard/genhdr/root_pointers.split
remote: GEN build-standard/genhdr/compressed.split
remote: GEN build-standard/genhdr/compressed.collected
remote: GEN build-standard/genhdr/moduledefs.collected
remote: GEN build-standard/genhdr/root_pointers.collected
remote: GEN build-standard/genhdr/qstrdefs.collected.h
remote: Compressed data updated
remote: GEN build-standard/genhdr/compressed.data.h
remote: Module registrations updated
remote: GEN build-standard/genhdr/moduledefs.h
remote: Root pointer registrations updated
remote: GEN build-standard/genhdr/root_pointers.h
remote: QSTR updated
remote: GEN build-standard/genhdr/qstrdefs.generated.h
....
remote: LINK build-standard/micropython
remote:    text    data     bss     dec     hex filename
remote:  752048   75256    7064  834368   cbb40 build-standard/micropython
remote: make: Leaving directory '/mnt/ssd/LOCAL_CI/micropython_CI/ports/unix'
remote: Running tests...
remote: make: Entering directory '/mnt/ssd/LOCAL_CI/micropython_CI/ports/unix'
remote: Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
remote: cd ../../tests && MICROPY_MICROPYTHON=../ports/unix/build-standard/micropython ./run-tests.py
....
remote: 639 tests performed (21150 individual testcases)
remote: 639 tests passed
remote: 31 tests skipped: annotate_var async_with async_with2 async_with_break async_with_return builtin_next_arg2 builtin_range_binop class_inplace_op2 del_deref del_local emg_exc exception_chain fun_name gen_yield_from_close generator_name heap_locked heapalloc_traceback io_buffered_writer memoryview_itemsize namedtuple_asdict nanbox_smallint opt_level_lineno schedule scope_implicit sys_getsizeof sys_path sys_tracebacklimit try_finally_return2 try_reraise try_reraise2 unboundlocal
remote: cat ../../tests/basics/0prelim.py | ./build-standard/micropython | grep -q 'abc'
remote: make: Leaving directory '/mnt/ssd/LOCAL_CI/micropython/ports/unix'
remote: multi_net/asyncio_tcp_client_rst.py on micropython|micropython: pass
remote: multi_net/asyncio_tcp_close_write.py on micropython|micropython: pass
remote: multi_net/asyncio_tcp_readall.py on micropython|micropython: pass
remote: multi_net/asyncio_tcp_readexactly.py on micropython|micropython: pass
remote: multi_net/asyncio_tcp_readinto.py on micropython|micropython: pass
remote: multi_net/asyncio_tcp_server_client.py on micropython|micropython: pass
remote: multi_net/asyncio_tls_server_client.py on micropython|micropython: pass
remote: multi_net/asyncio_tls_server_client_cert_required_error.py on micropython|micropython: pass
remote: multi_net/asyncio_tls_server_client_readline.py on micropython|micropython: pass
remote: multi_net/asyncio_tls_server_client_verify_error.py on micropython|micropython: pass
remote: multi_net/ssl_cert_ec.py on micropython|micropython: pass
remote: multi_net/ssl_cert_rsa.py on micropython|micropython: pass
remote: multi_net/sslcontext_check_hostname_error.py on micropython|micropython: pass
remote: multi_net/sslcontext_getpeercert.py on micropython|micropython: skip
remote: multi_net/sslcontext_server_client.py on micropython|micropython: pass
remote: multi_net/sslcontext_server_client_ciphers.py on micropython|micropython: pass
remote: multi_net/sslcontext_server_client_files.py on micropython|micropython: pass
remote: multi_net/sslcontext_verify_error.py on micropython|micropython: pass
remote: multi_net/sslcontext_verify_time_error.py on micropython|micropython: pass
remote: multi_net/tcp_accept_recv.py on micropython|micropython: pass
remote: multi_net/tcp_client_rst.py on micropython|micropython: pass
remote: multi_net/tcp_data.py on micropython|micropython: pass
remote: multi_net/udp_data.py on micropython|micropython: pass
remote: 23 tests performed
remote: 22 tests passed
remote: 1 tests skipped: multi_net/sslcontext_getpeercert.py
remote: N=1000 M=1000 n_average=8
remote: perf_bench/bm_chaos.py: 36270.75 0.6050 27571.43 0.6052
remote: perf_bench/bm_fannkuch.py: 72398.50 0.7372 110.51 0.7376
remote: perf_bench/bm_fft.py: 55118.88 0.6442 185788.00 0.6447
remote: perf_bench/bm_float.py: 32072.25 0.8578 467728.49 0.8589
remote: perf_bench/bm_hexiom.py: 24559.88 1.0508 1018.03 1.0572
remote: perf_bench/bm_nqueens.py: 26547.00 6.0596 377923.47 5.3878
remote: perf_bench/bm_pidigits.py: 36137.50 0.3131 13836.18 0.3123
remote: perf_bench/bm_wordcount.py: 133675.62 1.3903 598.58 1.4021
remote: perf_bench/core_import_mpy_multi.py: 8152.88 1.1345 61335.95 1.1335
remote: perf_bench/core_import_mpy_single.py: 88.75 0.7453 11268.23 0.7436
remote: perf_bench/core_locals.py: 206655.75 0.7563 387.14 0.7555
remote: perf_bench/core_qstr.py: 2271.00 2.4235 17623.62 2.3955
remote: perf_bench/core_str.py: 28647.12 1.1418 2094.72 1.1321
remote: perf_bench/core_yield_from.py: 10462.62 1.3926 19119.32 1.3757
remote: perf_bench/misc_aes.py: 36054.88 0.5909 28402.14 0.5901
remote: perf_bench/misc_mandel.py: 26755.25 0.8641 239223.11 0.8572
remote: perf_bench/misc_pystone.py: 23817.88 0.7204 167949.82 0.7214
remote: perf_bench/misc_raytrace.py: 21366.75 0.8452 45494.48 0.8431
remote: perf_bench/viper_call0.py: 10088.38 5.7759 29835.12 5.6861
remote: perf_bench/viper_call1a.py: 10519.00 5.3149 28603.73 5.5263
remote: perf_bench/viper_call1b.py: 13156.50 2.5998 22817.98 2.6244
remote: perf_bench/viper_call1c.py: 12976.38 3.2545 23143.22 3.2248
remote: perf_bench/viper_call2a.py: 10538.00 7.4143 28618.69 7.0926
remote: perf_bench/viper_call2b.py: 14392.50 3.9061 20875.40 3.8292
remote: OK
remote: UPDATED PATHS:
remote: extmod/extmod.cmake
remote: extmod/extmod.mk
remote: extmod/mbedtls/mbedtls_config_common.h
remote: lib/mbedtls
remote: lib/mbedtls_errors/mp_mbedtls_errors.c
remote: ports/mimxrt/mbedtls/mbedtls_config_port.h
remote: ports/mimxrt/mbedtls/mbedtls_port.c
remote: ports/renesas-ra/boards/ARDUINO_PORTENTA_C33/mbedtls_config_board.h
remote: ports/renesas-ra/mbedtls/mbedtls_config_port.h
remote: ports/renesas-ra/mbedtls/mbedtls_port.c
remote: ports/rp2/mbedtls/mbedtls_config_port.h
remote: ports/rp2/mbedtls/mbedtls_port.c
remote: ports/stm32/boards/ARDUINO_GIGA/mbedtls_config_board.h
remote: ports/stm32/boards/ARDUINO_NICLA_VISION/mbedtls_config_board.h
remote: ports/stm32/boards/ARDUINO_PORTENTA_H7/mbedtls_config_board.h
remote: ports/stm32/mbedtls/mbedtls_config_port.h
remote: ports/stm32/mbedtls/mbedtls_port.c
remote: ports/unix/mbedtls/mbedtls_config_port.h
remote: tests/README.md
remote: tests/multi_net/asyncio_tls_server_client.py
remote: tests/multi_net/asyncio_tls_server_client_cert_required_error.py
remote: tests/multi_net/asyncio_tls_server_client_readline.py
remote: tests/multi_net/asyncio_tls_server_client_verify_error.py
remote: tests/multi_net/ec_cert.der
remote: tests/multi_net/ec_key.der
remote: tests/multi_net/expired_cert.der
remote: tests/multi_net/rsa_cert.der
remote: tests/multi_net/rsa_key.der
remote: tests/multi_net/ssl_cert_ec.py
remote: tests/multi_net/ssl_cert_ec.py.exp
remote: tests/multi_net/ssl_cert_rsa.py
remote: tests/multi_net/ssl_data.py
remote: tests/multi_net/sslcontext_check_hostname_error.py
remote: tests/multi_net/sslcontext_getpeercert.py
remote: tests/multi_net/sslcontext_server_client.py
remote: tests/multi_net/sslcontext_server_client_ciphers.py
remote: tests/multi_net/sslcontext_server_client_files.py
remote: tests/multi_net/sslcontext_verify_error.py
remote: tests/multi_net/sslcontext_verify_time_error.py
remote:
To ssh://myserver.local/mnt/ssd/LOCAL_CI/micropython_CI/.git
 + 18bb03745...c4f384221 mbedtls3 -> mbedtls3 (forced update)

```

#### 7) Testing on devices.

Building, flashing and testing `stm32` port:
```
$ git cma --no-edit && git push -f
MicroPython codeformat.py for changed C files........(no files to check)Skipped
ruff.................................................(no files to check)Skipped
ruff-format..........................................(no files to check)Skipped
Spellcheck for changed files (codespell).............(no files to check)Skipped
MicroPython codeformat.py for changed C files............................Passed
MicroPython git commit message format checker............................Passed
- hook id: verifygitlog
- duration: 0.08s

ok

ruff.................................................(no files to check)Skipped
ruff-format..........................................(no files to check)Skipped
Spellcheck for changed files (codespell).................................Passed
[develop 7aeb80aba] ports/unix: Add install_user to Makefile.
 Date: Thu Feb 1 21:04:32 2024 +0000
 1 file changed, 7 insertions(+)
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Delta compression using up to 4 threads
Compressing objects: 100% (5/5), done.
Writing objects: 100% (5/5), 578 bytes | 578.00 KiB/s, done.
Total 5 (delta 4), reused 0 (delta 0), pack-reused 0
remote: GIT_WORK_TREE:  /mnt/ssd/DEV_CI/micropython
remote: /mnt/ssd/DEV_CI/micropython/.git
remote: checking out files...
remote: No local changes to save
remote: BRANCH:  develop
remote: TAG:  v1.23.0-preview-92-g7aeb80aba
remote: updating remote...
remote: done.
remote: GIT DIR:  /mnt/ssd/DEV_CI/micropython/.git
remote: UPDATED_PATHS:
remote: extmod/asyncio/stream.py
remote: ports/esp32/main.c
remote: ports/esp32/modnetwork.h
remote: ports/esp32/modnetwork_globals.h
remote: ports/esp32/network_wlan.c
remote: ports/unix/Makefile
remote: ports/unix/mbedtls/mbedtls_config_port.h
remote: tests/multi_net/asyncio_tcp_server_client_drain.py
remote: tests/multi_net/asyncio_tcp_server_client_drain.py.exp
remote:
remote: make: Entering directory '/mnt/ssd/DEV_CI/micropython/mpy-cross'
remote: Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
remote: GEN build/genhdr/mpversion.h
remote: GEN build/genhdr/qstrdefs.collected.h
remote: QSTR not updated
remote: GEN build/genhdr/moduledefs.collected
remote: Module registrations not updated
remote: GEN build/genhdr/root_pointers.collected
remote: Root pointer registrations not updated
remote: make: Leaving directory '/mnt/ssd/DEV_CI/micropython/mpy-cross'
remote: PORT: unix [ SKIP ]
remote: PORT: esp32 [ SKIP ]
remote: PORT: stm32 CI [ RUNNING ]
remote: Synchronizing submodule url for 'lib/libhydrogen'
remote: Synchronizing submodule url for 'lib/micropython-lib'
remote: Synchronizing submodule url for 'lib/stm32lib'
remote: MODE: [ Board Runner ]
remote: PORT: stm32 BOARDS: [boards]
remote: make: Entering directory '/mnt/ssd/DEV_CI/micropython/ports/stm32'
remote: Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
remote: rm -rf build-PYBV11
remote: make: Leaving directory '/mnt/ssd/DEV_CI/micropython/ports/stm32'
remote: make: Entering directory '/mnt/ssd/DEV_CI/micropython/ports/stm32'
remote: Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
remote: mkdir -p build-PYBV11/genhdr
remote: mkdir -p build-PYBV11/drivers/bus/
remote: mkdir -p build-PYBV11/drivers/dht/
remote: mkdir -p build-PYBV11/drivers/memory/
remote: mkdir -p build-PYBV11/extmod/
remote: mkdir -p build-PYBV11/lib/libm/
remote: mkdir -p build-PYBV11/lib/littlefs/
remote: mkdir -p build-PYBV11/lib/oofatfs/
remote: mkdir -p build-PYBV11/lib/stm32lib/CMSIS/STM32F4xx/Source/Templates/
remote: mkdir -p build-PYBV11/lib/stm32lib/CMSIS/STM32F4xx/Source/Templates/gcc/
remote: mkdir -p build-PYBV11/lib/stm32lib/STM32F4xx_HAL_Driver/Src/
remote: mkdir -p build-PYBV11/py/
remote: mkdir -p build-PYBV11/shared/libc/
remote: mkdir -p build-PYBV11/shared/netutils/
remote: mkdir -p build-PYBV11/shared/readline/
remote: mkdir -p build-PYBV11/shared/runtime/
remote: mkdir -p build-PYBV11/shared/timeutils/
remote: mkdir -p build-PYBV11/usbdev/class/src/
remote: mkdir -p build-PYBV11/usbdev/core/src/
remote: GEN build-PYBV11/genhdr/pins.h
remote: GEN build-PYBV11/genhdr/plli2stable.h
remote: GEN build-PYBV11/genhdr/pybcdc.inf
remote: GEN build-PYBV11/genhdr/pllfreqtable.h
remote: GEN stmconst build-PYBV11/genhdr/modstm_const.h
remote: GEN build-PYBV11/genhdr/pybcdc_inf.h
remote: GEN build-PYBV11/genhdr/mpversion.h
remote: GEN build-PYBV11/genhdr/qstr.i.last
remote: GEN build-PYBV11/genhdr/qstr.split
remote: GEN build-PYBV11/genhdr/moduledefs.split
remote: GEN build-PYBV11/genhdr/root_pointers.split
remote: GEN build-PYBV11/genhdr/compressed.split
remote: GEN build-PYBV11/genhdr/root_pointers.collected
remote: GEN build-PYBV11/genhdr/compressed.collected
remote: GEN build-PYBV11/genhdr/qstrdefs.collected.h
remote: GEN build-PYBV11/genhdr/moduledefs.collected
remote: Root pointer registrations updated
remote: GEN build-PYBV11/genhdr/root_pointers.h
remote: Compressed data updated
remote: GEN build-PYBV11/genhdr/compressed.data.h
remote: QSTR updated
remote: Module registrations updated
remote: GEN build-PYBV11/genhdr/qstrdefs.generated.h
remote: GEN build-PYBV11/genhdr/moduledefs.h
remote: AS ../../lib/stm32lib/CMSIS/STM32F4xx/Source/Templates/gcc/startup_stm32f405xx.s
remote: CC ../../lib/stm32lib/CMSIS/STM32F4xx/Source/Templates/system_stm32f4xx.c
remote: CC system_stm32.c
remote: AS resethandler.s
remote: AS ../../shared/runtime/gchelper_thumb2.s
remote: CC ../../py/mpstate.c
remote: CC ../../py/nlr.c
remote: CC ../../py/nlrx86.c
remote: CC ../../py/nlrx64.c
remote: CC ../../py/nlrthumb.c
remote: CC ../../py/nlraarch64.c
remote: CC ../../py/nlrmips.c
remote: CC ../../py/nlrpowerpc.c
remote: CC ../../py/nlrxtensa.c
remote: CC ../../py/nlrsetjmp.c
remote: CC ../../py/malloc.c
remote: CC ../../py/gc.c
remote: CC ../../py/pystack.c
remote: CC ../../py/qstr.c
remote: CC ../../py/vstr.c
remote: CC ../../py/mpprint.c
remote: CC ../../py/unicode.c
remote: CC ../../py/mpz.c
remote: CC ../../py/reader.c
remote: CC ../../py/lexer.c
remote: CC ../../py/parse.c
remote: CC ../../py/scope.c
remote: CC ../../py/compile.c
remote: CC ../../py/emitcommon.c
remote: CC ../../py/emitbc.c
remote: CC ../../py/asmbase.c
remote: CC ../../py/asmx64.c
remote: CC ../../py/emitnx64.c
remote: CC ../../py/asmx86.c
remote: CC ../../py/emitnx86.c
remote: CC ../../py/asmthumb.c
remote: CC ../../py/emitnthumb.c
remote: CC ../../py/emitinlinethumb.c
remote: CC ../../py/asmarm.c
remote: CC ../../py/emitnarm.c
remote: CC ../../py/asmxtensa.c
remote: CC ../../py/emitnxtensa.c
remote: CC ../../py/emitinlinextensa.c
remote: CC ../../py/emitnxtensawin.c
remote: CC ../../py/formatfloat.c
remote: CC ../../py/parsenumbase.c
remote: CC ../../py/parsenum.c
remote: CC ../../py/emitglue.c
remote: CC ../../py/persistentcode.c
remote: CC ../../py/runtime.c
remote: CC ../../py/runtime_utils.c
remote: CC ../../py/scheduler.c
remote: CC ../../py/nativeglue.c
remote: CC ../../py/pairheap.c
remote: CC ../../py/ringbuf.c
remote: CC ../../py/stackctrl.c
remote: CC ../../py/argcheck.c
remote: CC ../../py/warning.c
remote: CC ../../py/profile.c
remote: CC ../../py/map.c
remote: CC ../../py/obj.c
remote: CC ../../py/objarray.c
remote: CC ../../py/objattrtuple.c
remote: CC ../../py/objbool.c
remote: CC ../../py/objboundmeth.c
remote: CC ../../py/objcell.c
remote: CC ../../py/objclosure.c
remote: CC ../../py/objcomplex.c
remote: CC ../../py/objdeque.c
remote: CC ../../py/objdict.c
remote: CC ../../py/objenumerate.c
remote: CC ../../py/objexcept.c
remote: CC ../../py/objfilter.c
remote: CC ../../py/objfloat.c
remote: CC ../../py/objfun.c
remote: CC ../../py/objgenerator.c
remote: CC ../../py/objgetitemiter.c
remote: CC ../../py/objint.c
remote: CC ../../py/objint_longlong.c
remote: CC ../../py/objint_mpz.c
remote: CC ../../py/objlist.c
remote: CC ../../py/objmap.c
remote: CC ../../py/objmodule.c
remote: CC ../../py/objobject.c
remote: CC ../../py/objpolyiter.c
remote: CC ../../py/objproperty.c
remote: CC ../../py/objnone.c
remote: CC ../../py/objnamedtuple.c
remote: CC ../../py/objrange.c
remote: CC ../../py/objreversed.c
remote: CC ../../py/objset.c
remote: CC ../../py/objsingleton.c
remote: CC ../../py/objslice.c
remote: CC ../../py/objstr.c
remote: CC ../../py/objstrunicode.c
remote: CC ../../py/objstringio.c
remote: CC ../../py/objtuple.c
remote: CC ../../py/objtype.c
remote: CC ../../py/objzip.c
remote: CC ../../py/opmethods.c
remote: CC ../../py/sequence.c
remote: CC ../../py/stream.c
remote: CC ../../py/binary.c
remote: CC ../../py/builtinimport.c
remote: CC ../../py/builtinevex.c
remote: CC ../../py/builtinhelp.c
remote: CC ../../py/modarray.c
remote: CC ../../py/modbuiltins.c
remote: CC ../../py/modcollections.c
remote: CC ../../py/modgc.c
remote: CC ../../py/modio.c
remote: CC ../../py/modmath.c
remote: CC ../../py/modcmath.c
remote: CC ../../py/modmicropython.c
remote: CC ../../py/modstruct.c
remote: CC ../../py/modsys.c
remote: CC ../../py/moderrno.c
remote: CC ../../py/modthread.c
remote: CC ../../py/vm.c
remote: CC ../../py/bc.c
remote: CC ../../py/showbc.c
remote: CC ../../py/repl.c
remote: CC ../../py/smallint.c
remote: CC ../../py/frozenmod.c
remote: CC ../../extmod/machine_adc.c
remote: CC ../../extmod/machine_adc_block.c
remote: CC ../../extmod/machine_bitstream.c
remote: CC ../../extmod/machine_i2c.c
remote: CC ../../extmod/machine_i2s.c
remote: CC ../../extmod/machine_mem.c
remote: CC ../../extmod/machine_pinbase.c
remote: MPY asyncio/__init__.py
remote: MPY asyncio/core.py
remote: MPY asyncio/event.py
remote: MPY asyncio/funcs.py
remote: MPY asyncio/lock.py
remote: MPY asyncio/stream.py
remote: MPY uasyncio.py
remote: MPY dht.py
remote: MPY onewire.py
remote: MPY lcd160cr.py
remote: GEN build-PYBV11/frozen_content.c
remote: CC ../../extmod/machine_pulse.c
remote: CC ../../extmod/machine_pwm.c
remote: CC ../../extmod/machine_signal.c
remote: CC ../../extmod/machine_spi.c
remote: CC ../../extmod/machine_timer.c
remote: CC ../../extmod/machine_uart.c
remote: CC ../../extmod/machine_wdt.c
remote: CC ../../extmod/modasyncio.c
remote: CC ../../extmod/modbinascii.c
remote: CC ../../extmod/modbluetooth.c
remote: CC ../../extmod/modbtree.c
remote: CC ../../extmod/modcryptolib.c
remote: CC ../../extmod/moddeflate.c
remote: CC ../../extmod/modframebuf.c
remote: CC ../../extmod/modhashlib.c
remote: CC ../../extmod/modheapq.c
remote: CC ../../extmod/modjson.c
remote: CC ../../extmod/modlwip.c
remote: CC ../../extmod/modmachine.c
remote: CC ../../extmod/modnetwork.c
remote: CC ../../extmod/modonewire.c
remote: CC ../../extmod/modos.c
remote: CC ../../extmod/modplatform.c
remote: CC ../../extmod/modrandom.c
remote: CC ../../extmod/modre.c
remote: CC ../../extmod/modselect.c
remote: CC ../../extmod/modsocket.c
remote: CC ../../extmod/modssl_axtls.c
remote: CC ../../extmod/modssl_mbedtls.c
remote: CC ../../extmod/modtime.c
remote: CC ../../extmod/moductypes.c
remote: CC ../../extmod/modwebrepl.c
remote: CC ../../extmod/modwebsocket.c
remote: CC ../../extmod/network_cyw43.c
remote: CC ../../extmod/network_esp_hosted.c
remote: CC ../../extmod/network_lwip.c
remote: CC ../../extmod/network_ninaw10.c
remote: CC ../../extmod/network_wiznet5k.c
remote: CC ../../extmod/os_dupterm.c
remote: CC ../../extmod/vfs.c
remote: CC ../../extmod/vfs_blockdev.c
remote: CC ../../extmod/vfs_fat.c
remote: CC ../../extmod/vfs_fat_diskio.c
remote: CC ../../extmod/vfs_fat_file.c
remote: CC ../../extmod/vfs_lfs.c
remote: CC ../../extmod/vfs_posix.c
remote: CC ../../extmod/vfs_posix_file.c
remote: CC ../../extmod/vfs_reader.c
remote: CC ../../extmod/virtpin.c
remote: CC ../../shared/libc/abort_.c
remote: CC ../../shared/libc/printf.c
remote: CC ../../lib/oofatfs/ff.c
remote: CC ../../lib/oofatfs/ffunicode.c
remote: CC ../../lib/littlefs/lfs2.c
remote: CC ../../lib/littlefs/lfs2_util.c
remote: CC ../../lib/libm/acoshf.c
remote: CC ../../lib/libm/asinfacosf.c
remote: CC ../../lib/libm/asinhf.c
remote: CC ../../lib/libm/atan2f.c
remote: CC ../../lib/libm/atanf.c
remote: CC ../../lib/libm/atanhf.c
remote: CC ../../lib/libm/ef_rem_pio2.c
remote: CC ../../lib/libm/erf_lgamma.c
remote: CC ../../lib/libm/fmodf.c
remote: CC ../../lib/libm/kf_cos.c
remote: CC ../../lib/libm/kf_rem_pio2.c
remote: CC ../../lib/libm/kf_sin.c
remote: CC ../../lib/libm/kf_tan.c
remote: CC ../../lib/libm/log1pf.c
remote: CC ../../lib/libm/math.c
remote: CC ../../lib/libm/nearbyintf.c
remote: CC ../../lib/libm/roundf.c
remote: CC ../../lib/libm/sf_cos.c
remote: CC ../../lib/libm/sf_erf.c
remote: CC ../../lib/libm/sf_frexp.c
remote: CC ../../lib/libm/sf_ldexp.c
remote: CC ../../lib/libm/sf_modf.c
remote: CC ../../lib/libm/sf_sin.c
remote: CC ../../lib/libm/sf_tan.c
remote: CC ../../lib/libm/wf_lgamma.c
remote: CC ../../lib/libm/wf_tgamma.c
remote: CC ../../lib/libm/thumb_vfp_sqrtf.c
remote: CC ../../shared/libc/string0.c
remote: CC ../../shared/netutils/dhcpserver.c
remote: CC ../../shared/netutils/netutils.c
remote: CC ../../shared/netutils/trace.c
remote: CC ../../shared/readline/readline.c
remote: CC ../../shared/runtime/gchelper_native.c
remote: CC ../../shared/runtime/interrupt_char.c
remote: CC ../../shared/runtime/mpirq.c
remote: CC ../../shared/runtime/pyexec.c
remote: CC ../../shared/runtime/softtimer.c
remote: CC ../../shared/runtime/stdout_helpers.c
remote: CC ../../shared/runtime/sys_stdio_mphal.c
remote: CC ../../shared/timeutils/timeutils.c
remote: CC ../../drivers/bus/softspi.c
remote: CC ../../drivers/bus/softqspi.c
remote: CC ../../drivers/memory/spiflash.c
remote: CC ../../drivers/dht/dht.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_adc.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_adc_ex.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_cortex.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_dma.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_flash.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_flash_ex.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_gpio.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_i2c.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_pwr.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_pwr_ex.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_rcc.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_rcc_ex.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_rtc.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_rtc_ex.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_spi.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_tim.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_tim_ex.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_uart.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_ll_rcc.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_ll_utils.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_pcd.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_pcd_ex.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_ll_usb.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_sd.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_ll_sdmmc.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_ll_fmc.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_mmc.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_sdram.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_dcmi.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_dma_ex.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_can.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_i2s.c
remote: CC ../../lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_i2s_ex.c
remote: CC usbdev/core/src/usbd_core.c
remote: CC usbdev/core/src/usbd_ctlreq.c
remote: CC usbdev/core/src/usbd_ioreq.c
remote: CC usbdev/class/src/usbd_cdc_msc_hid.c
remote: CC usbdev/class/src/usbd_msc_bot.c
remote: CC usbdev/class/src/usbd_msc_scsi.c
remote: CC boardctrl.c
remote: CC main.c
remote: CC stm32_it.c
remote: CC usbd_conf.c
remote: CC usbd_desc.c
remote: CC usbd_cdc_interface.c
remote: CC usbd_hid_interface.c
remote: CC usbd_msc_interface.c
remote: CC mphalport.c
remote: CC mpnetworkport.c
remote: CC mpthreadport.c
remote: CC irq.c
remote: CC pendsv.c
remote: CC systick.c
remote: CC powerctrl.c
remote: CC powerctrlboot.c
remote: CC rfcore.c
remote: CC pybthread.c
remote: CC factoryreset.c
remote: CC timer.c
remote: CC led.c
remote: CC pin.c
remote: CC pin_defs_stm32.c
remote: CC pin_named_pins.c
remote: CC bufhelper.c
remote: CC dma.c
remote: CC i2c.c
remote: CC pyb_i2c.c
remote: CC spi.c
remote: CC pyb_spi.c
remote: CC qspi.c
remote: CC octospi.c
remote: CC uart.c
remote: CC ulpi.c
remote: CC can.c
remote: CC fdcan.c
remote: CC pyb_can.c
remote: CC usb.c
remote: CC eth.c
remote: CC gccollect.c
remote: CC help.c
remote: CC machine_bitstream.c
remote: CC machine_i2c.c
remote: CC machine_spi.c
remote: CC modpyb.c
remote: CC modstm.c
remote: CC network_lan.c
remote: CC extint.c
remote: CC usrsw.c
remote: CC rng.c
remote: CC rtc.c
remote: CC flash.c
remote: CC flashbdev.c
remote: CC spibdev.c
remote: CC storage.c
remote: CC sdcard.c
remote: CC sdram.c
remote: CC fatfs_port.c
remote: CC lcd.c
remote: CC accel.c
remote: CC servo.c
remote: CC dac.c
remote: CC adc.c
remote: CC sdio.c
remote: CC subghz.c
remote: CC build-PYBV11/pins_PYBV11.c
remote: CC build-PYBV11/frozen_content.c
remote: LINK build-PYBV11/firmware.elf
remote:    text    data     bss     dec     hex filename
remote:  365852      52   27436  393340   6007c build-PYBV11/firmware.elf
remote: GEN build-PYBV11/firmware0.bin
remote: GEN build-PYBV11/firmware1.bin
remote: GEN build-PYBV11/firmware.hex
remote: GEN build-PYBV11/firmware.dfu
remote: make: Leaving directory '/mnt/ssd/DEV_CI/micropython/ports/stm32'
remote: PORT: stm32 BOARD: PYBV11  BUILD [ OK ]
remote: make: Entering directory '/mnt/ssd/DEV_CI/micropython/ports/stm32'
remote: Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
remote: Writing build-PYBV11/firmware.dfu to the board
remote: File: build-PYBV11/firmware.dfu
remote:     b'DfuSe' v1, image size: 366213, targets: 1
remote:     b'Target' 0, alt setting: 0, name: "ST...", size: 365928, elements: 2
remote:       0, address: 0x08000000, size: 14872
remote:       1, address: 0x08020000, size: 351040
remote:     usb: 0483:df11, device: 0x0000, dfu: 0x011a, b'UFD', 16, 0x2f7dea30
remote: Writing memory...
remote: 0x08000000   14872 [=========================] 100%
remote: 0x08020000  351040 [=========================] 100%
remote: Exiting DFU...
remote: Finished
remote: make: Leaving directory '/mnt/ssd/DEV_CI/micropython/ports/stm32'
remote: PORT: stm32 BOARD: PYBV11  FIRMWARE FLASH [ OK ]
remote: PORT: stm32 BOARD: PYBV11  Running custom tests...
remote: pass  /mnt/ssd/DEV_CI/micropython-localCI/hw_tests/ports/stm32/boards/PYBV11/i2c/i2c_scan.py
remote: 1 tests performed (2 individual testcases)
remote: 1 tests passed
remote: PORT: stm32 BOARD: PYBV11 TEST: TEST_I2C [ OK ]
remote: PORT: stm32 BOARD: PYBV11 TEST: RESET [ OK ]
remote: PORT: stm32 BOARDS: [production_boards]
remote: PORT: stm32 BOARD: PYB_DEV  BUILD [ SKIP ]
remote: PORT: stm32 BOARD: PYB_DEV  Running custom tests...
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/uart.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/timer_callback.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/timer.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/switch.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/spi.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/servo.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/rtc.py
remote: skip  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/pyb_f411.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/pyb_f405.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/pyb1.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/pin.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/modtime.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/modstm.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/led.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/irq.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/i2c_error.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/i2c_accel.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/i2c.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/extint.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/dac.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/can2.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/can.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/board_pybv1x.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/adcall.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/adc.py
remote: pass  /mnt/ssd/DEV_CI/micropython/tests/ports/stm32/accel.py
remote: 25 tests performed (322 individual testcases)
remote: 25 tests passed
remote: 1 tests skipped: pyb_f411
remote: PORT: stm32 BOARD: PYB_DEV TEST: TEST_HW_PYB [ OK ]
remote: PORT: stm32 BOARD: PYB_DEV TEST: RESET [ OK ]
remote: SUCCESS! in production_boards
remote: Done
remote: Done
remote: PORT: stm32 [ OK ]
remote: PORT: rp2 [ SKIP ]
To ssh://amd.local/mnt/ssd/DEV_CI/micropython/.git
 + 0a282fb56...7aeb80aba develop -> develop (forced update)
```

See `./local_ci_stm32.sh`

If using Linux and `Access denied (insufficient permissions)` is raised trying to set the bootloader mode do 
```
$ sudo usermod -a -G dialout $USER
```
or flashing the firmware see [this solution](https://askubuntu.com/questions/1048870/permission-denied-to-non-root-user-for-usb-device) which requires adding a udev rule e.g.

```
$ sudoedit /etc/udev/rules.d/99-dfu.rules
```
add (check idVendor and idProduct with lsusb, format is ID idVendor:idProduct)


```SUBSYSTEMS=="usb", ATTR{idVendor}=="0483", ATTR{idProduct}=="df11", MODE="666"```

then 
```
$ sudo udevadm control --reload-rules && sudo udevadm trigger
$ sudo service udev restart
```
Finally unplug and replug the USB device, then it should work.


#### 8) Using environment variables:

Modify the default `.env` file installed in remote `./micropython_CI` repo (or create one) 

Set options for the local CI:
`LOCAL_CI_PATH` path where local CI scripts are, the default is `../micropython-localCI`

`LOCAL_CI_PORTS` set a default set of ports to run, the default is `unix` ( implemented ports are `unix`, `stm32` and `esp32` at the moment)

`LOCAL_CI_PARALLEL` whether to run ports CI in parallel, default is `False`. If set to `True` the output will be redirected to `<port>.log` in remote repo CI top dir.
> [!WARNING]
> Experimental, it may not work as expected

`LOCAL_CI_PARALLEL_BOARDS` whether to run ports CI boards in parallel, default is `False`. If set to `True` the output will be redirected to `<port>_<board>.log` in remote repo CI top dir.
> [!WARNING]
> Experimental, it may not work as expected


`<PORT>_BOARD_RUNNER` to use `./board_runner.py` which allows to build, flash and test multiple boards
`<PORT>_BOARDS_CONFIG` path to the port boards config file defaults to `$LOCAL_CI_PATH/config/<PORT>_boards.yaml`

#### Defaults if not using BOARD_RUNNER
- `<PORT>_DEVICE` to indicate the USB port of the DTU (required for flashing and testing).
- `<PORT>_FLASH` to indicate if the firmware should be flashed for this port, default to `True`.
- `<PORT>_TEST` to indicate if tests should be run for this port, default to `True`.
- `<PORT>_TEST_BOARD` to indicate target name for `./run-tests.py` script.


See default `.env`
```dot
# CI options
export LOCAL_CI_PATH="../micropython-localCI"
export LOCAL_CI_PORTS="unix" # to run other ports e.g. "unix esp32 stm32" 
export LOCAL_CI_PARALLEL="False"  # experimental
export LOCAL_CI_PARALLEL_BOARDS="False"  # experimental

# BOARDS
# To add your custom boards
# export MY_BOARDS="<path_to_your_boards>"

# PORTS 

# ESP32
export ESP32_BOARD_RUNNER="True"
export ESP32_BOARDS_CONFIG=$LOCAL_CI_PATH/config/esp32_boards.yaml
# To set the BOARD_DIR to your custom boards, defaults to ports/esp32/boards
# e.g.
# export ESP32_BOARD_DIR=$PWD/../$MY_BOARDS

# Defaults if not using BOARD_RUNNER
export ESP32_BOARD_DIR=$PWD/ports/esp32/boards
export ESP32_BOARD="ESP32_GENERIC"
export ESP32_DEVICE="/dev/ttyUSB0" 
export ESP32_FLASH="True"
export ESP32_TEST="True"
export ESP32_TEST_BOARD="esp32"

# STM32
export STM32_BOARD_RUNNER="True"
export STM32_BOARDS_CONFIG=$LOCAL_CI_PATH/config/stm32_boards.yaml
# To set the BOARD_DIR to your custom boards, defaults to ports/stm32/boards
# e.g.
# export STM32_BOARD_DIR=$PWD/../$MY_BOARDS

# Defaults if not using BOARD_RUNNER
export STM32_BOARD_DIR=$PWD/ports/stm32/boards
export STM32_BOARD="PYBV11"
export STM32_DEVICE="/dev/ttyACM0" 
export STM32_FLASH="True"
export STM32_TEST="True"
export STM32_TEST_BOARD="stm32"

# UNIX 
# export UNIX_VARIANT="standard" 
# export UNIX_VARIANT_DIR=$PWD/ports/unix/variants 


```

And default stm32 port boards config file: 
```yaml

boards:
 PYBV11:
     BUILD: true
     FLASH: true
     TEST: true # ./run-tests.py
     JOBS: 10
     PORT: "/dev/ttyACM0"
     BOOTLOADER: "tools/mpremote/mpremote.py a0 bootloader"
     CUSTOM_TESTS:

        TEST_HW:
         test_dir: "$PWD/tests/ports/stm32"
         test_files: "*.py"
         cmd: "./run-tests.py $test_dir/$test_files --target pyboard --device $PORT"
         cwd: "./tests"
         env_path: ""

        RESET:
         cmd: "./tools/mpremote/mpremote.py a0 reset"

```

#### 9) Running custom tests


In a `<port>_boards.yaml` config file is possible to define custom tests to run
defining `CUSTOM_TESTS` e.g. `esp32_boards.yaml` running hardware and
multitests:

```yaml
boards:
 ESP32_GENERIC:
     JOBS: 8
     BUILD: true
     FLASH: true
     TEST: true # --> ./run-tests.py
     PORT: "/dev/ttyUSB0"
     CUSTOM_TESTS:  

       TEST_HW: 
        test_dir: "$PWD/tests/ports/esp32"
        test_files: "*.py"
        cmd: "./run-tests.py $test_dir/$test_files --target esp32 --device $PORT"
        cwd: "./tests"
        env_path: ""

       TEST_MULTINET: 
        test_dir: "$PWD/tests/multi_net"
        test_files: "*.py"
        cmd: "./run-multitests.py $test_dir/$test_files -i pyb:$PORT"
        cwd: "./tests"
        env_path: ""

       TEST_MULTIBLUETOOTH: 
        test_dir: "$PWD/tests/multi_bluetooth"
        test_files: "*.py"
        cmd: "./run-multitests.py $test_dir/$test_files -i pyb:$PORT"
        cwd: "./tests"
        env_path: ""

       RESET:
         cmd: "./tools/mpremote/mpremote.py reset u0"
     CALLBACKS:
      on_success:
       cmd: "echo 'SUCCESS!'"
      on_error:
       cmd: "echo 'FAILED! '"

```

#### 10) Using board groups, multiple boards and success/errors callbacks

In a `<port>_boards.yaml` config file is possible to use multiple boards and
boards groups. Default board group is `boards`.

It's also possible to define custom callbacks that can be triggered if the
build/flash/test process (BFT) is successful or not, e.g. in this case if the "test" `PYBV11`
board BFT is successful, it will trigger the BFT process of
`production_boards`.
```yaml

boards:
 PYBV11:
     BUILD: true
     FLASH: true
     TEST: true
     JOBS: 10
     BOOTLOADER: "tools/mpremote/mpremote.py a0 bootloader"
     PORT: "/dev/ttyACM0"
     CUSTOM_TESTS:
         TEST_HW_PYB: 
          test_dir: "$PWD/tests/ports/stm32"
          test_files: "*.py"
          cmd: "./run-tests.py $test_dir/$test_files --target pyboard --device $PORT"
          cwd: "./tests"
          env_path: ""

         RESET:
         cmd: "./tools/mpremote/mpremote.py a0 reset"
     
     CALLBACKS:
      on_success: 
        cmd: "$LOCAL_CI_PATH/board_runner.py stm32 --boards production_boards"
      on_error:
        cmd: "echo 'ERROR in test boards aborting production_boards'"
 
 PYBLITEV10:
     BUILD: false
     FLASH: false
     TEST: false
     JOBS: 10
     BOOTLOADER: "tools/mpremote/mpremote.py a2 bootloader"
     PORT: "/dev/ttyACM2"
     CUSTOM_TESTS:
         TEST_HW_PYB: 
          test_dir: "$PWD/tests/ports/stm32"
          test_files: "*.py"
          cmd: "./run-tests.py $test_dir/$test_files --target pyboard --device $PORT"
          cwd: "./tests"
          env_path: ""

         RESET:
         cmd: "./tools/mpremote/mpremote.py a2 reset"


production_boards:
 PYB_DEV:
     BUILD: true
     FLASH: true
     TEST: true
     JOBS: 10
     BOOTLOADER: "tools/mpremote/mpremote.py a1 bootloader"
     PORT: "/dev/ttyACM1"
     CUSTOM_TESTS:
        TEST_HW_PYB: 
         test_dir: "$PWD/tests/ports/stm32"
         test_files: "*.py"
         cmd: "./run-tests.py $test_dir/$test_files --target pyboard --device $PORT"
         cwd: "./tests"
         env_path: ""
        RESET:
         cmd: "./tools/mpremote/mpremote.py a1 reset"
     CALLBACKS:
      on_success:
        cmd: "echo 'SUCCESS! in production_boards'"
```



