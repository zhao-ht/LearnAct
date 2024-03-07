(define (problem tyreworld-9)
(:domain tyreworld)
(:objects 
wrench jack pump - tool
the-hub1 the-hub2 the-hub3 the-hub4 - hub
nuts1 nuts2 nuts3 nuts4 - nut
boot - container
r1 w1 r2 w2 r3 w3 r4 w4 - wheel
)
(:init
(in jack boot)
(in pump boot)
(in wrench boot)
(unlocked boot)
(closed boot)
(intact r1)
(in r1 boot)
(not-inflated r1)
(intact r2)
(in r2 boot)
(not-inflated r2)
(intact r3)
(in r3 boot)
(not-inflated r3)
(intact r4)
(in r4 boot)
(not-inflated r4)
(on w1 the-hub1)
(on-ground the-hub1)
(tight nuts1 the-hub1)
(fastened the-hub1)
(on w2 the-hub2)
(on-ground the-hub2)
(tight nuts2 the-hub2)
(fastened the-hub2)
(on w3 the-hub3)
(on-ground the-hub3)
(tight nuts3 the-hub3)
(fastened the-hub3)
(on w4 the-hub4)
(on-ground the-hub4)
(tight nuts4 the-hub4)
(fastened the-hub4)
)
(:goal
(and
(in w3 boot)
(in w4 boot)
)
)
)

