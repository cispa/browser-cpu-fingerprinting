(module
    (import "env" "mem" (memory 1024 1024 shared))
    (import "console" "log" (func $log (param i32)))
    (export "iterate" (func $iterate))
    (export "check" (func $check))
    (export "write" (func $write))

    (func $iterate (param $start i32) (param $iterations i64) (result i64)
        (local $head i32)
        (local $i i64)
        (local $t0 i64)
        (local.set $i (i64.const 1))
        (local.set $head (local.get $start))

        (local.set $t0 (i64.load (i32.const 256)))

        (loop $iter
            (local.set $head (i32.load (local.get $head)))
            (local.set $i (i64.add (local.get $i) (i64.const 1)))
            (br_if $iter (i64.lt_u (local.get $i) (local.get $iterations)))
        )

        (i64.load (i32.const 256))
        (local.get $t0)
        (i64.sub)

        return
    )

    (func $check (param $start i32) (result i64)
        (local $head i32)
        (local $i i64)
        (local.set $i (i64.const 0))
        (local.set $head (local.get $start))

        (loop $iter
            ;; (local.get $head)
            ;; (call $log)
            (local.set $head (i32.load (local.get $head)))
            (local.set $i (i64.add (local.get $i) (i64.const 1)))
            (br_if $iter (i32.ne (local.get $head) (local.get $start)))
        )

        (local.get $i)
        return
    )

    (func $write (param $ptr i32) (param $value i32)

        (i32.store (local.get $ptr) (local.get $value))

        return
    )
)