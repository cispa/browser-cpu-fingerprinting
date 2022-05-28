(module
    (import "env" "mem" (memory 1024 1024 shared))
    (import "console" "log" (func $log (param i32)))
    (export "maccess" (func $maccess))
    (export "write" (func $write))

    (func $maccess (param $ptr i32) (param $offset i32) (param $fence i32) (result i64)
        (local $t0 i64)
        (local $tmp i32)

        (local.set $tmp (i32.load (local.get $ptr)))

        ;; fence
        (loop $iter
            (local.set $fence (i32.sub (local.get $fence) (i32.const 1)))
            (br_if $iter (i32.gt_u (local.get $fence) (i32.const 0)))
        )

        ;; start
        (local.set $t0 (i64.load (i32.const 256)))

        (local.set $tmp (i32.load (i32.add (local.get $ptr) (local.get $offset))))

        ;; time
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