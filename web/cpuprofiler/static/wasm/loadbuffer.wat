(module
    (import "env" "mem" (memory 1024 1024 shared))
    (import "console" "log" (func $log (param i32)))
    (export "routine" (func $routine))

    (func $routine (param $p1 i32) (param $p2 i32) (param $iterations i32) (result i64)
        (local $t0 i64)
        (local $tmp i32)

        (local.set $t0 (i64.load (i32.const 256)))

        ;; actual routine
        (loop $iter

            ;; cache miss
            (local.set $p1 (i32.load (local.get $p1)))

            (i32.const 0)
            ;; split here
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))

            ;; cache miss
            (local.set $p2 (i32.load (local.get $p2)))

            (local.set $tmp)
            (i32.const 0)

            ;; split here
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))
            (i32.add (i32.load (i32.const 0)))

            (local.set $tmp)

            (local.set $iterations (i32.sub (local.get $iterations) (i32.const 1)))
            (br_if $iter (i32.gt_u (local.get $iterations) (i32.const 0)))
        )

        (i64.load (i32.const 256))
        (local.get $t0)
        (i64.sub)

        return
    )
)