#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

struct pcg_state_setseq_64 {    // Internals are *Private*.
    uint64_t state;             // RNG state.  All values are possible.
    uint64_t inc;               // Controls which RNG sequence (stream) is
    // selected. Must *always* be odd.
};
typedef struct pcg_state_setseq_64 pcg32_random_t;
static pcg32_random_t pcg32_global = { 0x853c49e6748fea9bULL, 0xda3e39cb94b95bdbULL };

static inline uint32_t pcg32_random_r(pcg32_random_t* rng) {
    uint64_t oldstate = rng->state;
    rng->state = oldstate * 6364136223846793005ULL + rng->inc;
    uint32_t xorshifted = (uint32_t)(((oldstate >> 18u) ^ oldstate) >> 27u);
    uint32_t rot = oldstate >> 59u;
    return (xorshifted >> rot) | (xorshifted << ((-rot) & 31));
}

static inline uint32_t pcg32_random(void) {
    return pcg32_random_r(&pcg32_global);
}


static inline void pcg32_init_state(uint64_t state) {
    pcg32_global.state = state;
}

static inline void pcg32_init_inc(uint64_t inc) {
    pcg32_global.inc = inc | 1;
}

static inline uint32_t pcg32_random_bounded_divisionless(uint32_t range) {
    uint64_t random32bit, multiresult;
    uint32_t leftover;
    uint32_t threshold;
    random32bit =  pcg32_random();
    multiresult = random32bit * range;
    leftover = (uint32_t) multiresult;
    if(leftover < range ) {
        threshold = -range % range ;
        while (leftover < threshold) {
            random32bit =  pcg32_random();
            multiresult = random32bit * range;
            leftover = (uint32_t) multiresult;
        }
    }
    return multiresult >> 32; // [0, range)
}

int main(int argc, char **argv) {
  uint32_t week[7];

  const uint32_t N = 1000000;
  uint32_t count = 0;

  clock_t tic = clock();

  for (int i = 0; i < N; i++) {
    for (int j = 0; j < 7; j++) { week[j] = 0; }

    /* Simulate 12 phone calls */
    uint32_t idx = 0;
    for (int j = 0; j < 12; j++) {
      idx = pcg32_random_bounded_divisionless(7);
      week[idx]++;
    }

    /* Check if every day had atleast one phone call */
    for (int j = 0; j < 7; j++) {
      if (week[j] == 0) { count++; break; }
    }
  }

  clock_t toc = clock();
    
  printf("answer = %f, duration = %.0fms\n",
	 (float) (N-count) / N,
	 (double) (toc - tic) / CLOCKS_PER_SEC * 1000);

  return 0;
}
