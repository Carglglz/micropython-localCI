### Setup a local CI runner 

Automate CI builds/tests runs in the local computer or a local/private server (accessed using SSH) 

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

Copy git hooks from `tools/local_ci/git_hooks` into `.git/hooks`

```
$ cp tools/local_ci/git_hooks/post-*  .git/hooks/
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

See `local_ci/local_ci_stm32.sh`

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

Create a `.env` file in top dir of remote `local MicroPython CI` repo. 

Set options for the local CI:
`LOCAL_CI_PATH` path where local CI scripts are, the default is `tools/local_ci`

`LOCAL_CI_PORTS` set a default set of ports to run, the default is `all` (unix, stm32, esp32, rp2 at the moment)

`LOCAL_CI_PARALLEL` whether to run ports CI in parallel, default is `False`. If set to `True` the output will be redirect to `<port>.log` in remote repo top dir.

`<PORT>_DEVICE` to indicate the USB port of the DTU (required for flashing and testing)
`<PORT>_FLASH` to indicate if the firmware should be flashed for this port, default to `True`
`<PORT>_TEST` to indicate if tests should be run for this port, default to `True`


