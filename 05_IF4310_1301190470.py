import random
import math
import matplotlib.pyplot as plot

#creating populasi
def make_pop (len_chrom, n_pop):
  pop = []
  for i in range(n_pop):
    chrom = []
    for j in range(len_chrom):
      chrom.append(random.randint(0,9))
    pop.append(chrom)
  return pop

#decoding integer chromosom 
def decode_chrom (chrom, minmaxx, minmaxy):
  half_chrom = len(chrom) // 2

  chrom_x = chrom[:half_chrom]
  len_x = len(chrom_x)

  top_x = 0
  bot_x = 0
  for i in range(len_x):
    top_x += chrom_x[i] * 10**-(i+1)
    bot_x += 9 * 10 **-(i+1)

  x = minmaxx["min"] + (top_x * (minmaxx["max"] - minmaxx["min"]) / bot_x)
  
  chrom_y = chrom[half_chrom:]
  len_y = len(chrom_y)

  top_y = 0
  bot_y = 0
  for i in range(len_y):
    top_y += chrom_y[i] * 10**-(i+1)
    bot_y += 9 * 10**-(i+1)

  y = minmaxy["min"] + (top_y * (minmaxy["max"] - minmaxy["min"]) / bot_y)
  return x, y

#fitness value
def fitness(x, y):
  return (math.cos(x**2) * math.sin(y**2)) + (x + y)

#fitness population
def fitness_pop(pop):
  fit_pop = []
  for chrom in pop:
    x, y = decode_chrom(chrom, minmaxx, minmaxy)
    fit_pop.append(fitness(x, y))
  return fit_pop

#select parent tournament methode
def select_parent (pop, fit_pop):
  k = 10
  t = 2
  tourney_pop, tourney_fit = [], []
  #select random from pop
  for i in range(k):
    r = random.randint(0, len_chrom)
    tourney_pop.append(pop[r])
    tourney_fit.append(fit_pop[r])
  #select best from tourney
  best = [k for i, k in sorted(zip(tourney_fit, tourney_pop), reverse = True)[:t]]
  return best

#crossover two point methode
def crossover(parent):
  bound = (len_chrom // 2)
  cross_p1 = random.randint(0, bound)
  cross_p2 = random.randint(bound, len_chrom)
  offspring = [[], []]

  offspring[0] = parent[0][:cross_p1]+parent[1][cross_p1:cross_p2]+parent[0][cross_p2:]
  offspring[1] = parent[1][:cross_p1]+parent[0][cross_p1:cross_p2]+parent[1][cross_p2:]

  return offspring

#mutation
def mutation (offspring):
  prob = 0.1
  child = offspring
  for i in range(len(child)):
    for j in range(len_chrom):
      if random.uniform(0, 1) <= prob:
        mutate = random.randint(0, 9)
        child[i][j] = mutate
  return child

#probabilitas crossover 
prob_cross = 0.7

#panjang kromosom
len_chrom = 10

#banyaknya populasi
n_pop = 100

#elitisme
n_elite = 2

#max generation
n_gen = 500

#batasan
minmaxx = {
    "min" : -1,
    "max" : 2
}
minmaxy = {
    "min" : -1,
    "max" : 1
}

#random.seed(10)
best_gen = []
pop = make_pop(len_chrom, n_pop)

for i in range(n_gen):
  fit_pop = fitness_pop(pop)
  
  best_gen.append(max(fit_pop))

  sort_pop = [k for p, k in sorted(zip(fit_pop, pop), reverse = True)]

  new_pop = sort_pop[:n_elite]
  print(f"Best of Generation-{i+1}: ")
  print(f" Chromosom: {sort_pop[0]} \n fitnexx = {best_gen[i]}")
  xb, yb = decode_chrom(sort_pop[0], minmaxx, minmaxy)
  print(f"  x value: {xb} \n  y value: {yb}")
  print(f"---------------------------------------") 

  while len(new_pop) < n_pop:
    parent = select_parent(pop, fit_pop)

    if random.random() < prob_cross:
      child = mutation(crossover(parent))
    else:
      child = parent + []

    new_pop = new_pop + child
  
  pop = new_pop

plot.plot(range(1, n_gen + 1), best_gen)
plot.xlabel("Generasi")
plot.ylabel("Fitness")
plot.show()