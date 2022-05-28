(module
    (import "env" "mem" (memory 1024 1024 shared))
    (import "console" "log" (func $log (param i32)))
    (export "maccess" (func $maccess))
    (export "write" (func $write))

    (func $maccess (param $ptr i32) (result i64)
        (local $t0 i64)
        (local $tmp i32)

        (local.set $t0 (i64.load (i32.const 256)))

        (local.set $tmp (i32.load (local.get $ptr)))

        (i64.load (i32.const 256))
        (local.get $t0)
        (i64.sub)

        return
    )

    (func $write (param $ptr i32) (param $value i32)

        (i32.store (local.get $ptr) (local.get $value))

        return
    )
)