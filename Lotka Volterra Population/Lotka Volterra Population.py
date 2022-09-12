import numpy as np
import matplotlib.pyplot as plt


def prey(prey_pop, predator_pop, k_m, k_mf):
    return prey_pop * (k_m - k_mf * predator_pop)  # dm/dt


def predator(prey_pop, predator_pop, k_f, k_fm):
    return predator_pop * (-k_f + k_fm * prey_pop)  # df/dt


def explicit_euler(p1, p2, n, h, k_m, k_mf, k_f, k_fm):
    prey_pop = [p1]
    predator_pop = [p2]
    for i in range(n):
        p1 = p1 + h * prey(p1, p2, k_m, k_mf)
        p2 = p2 + h * predator(p1, p2, k_f, k_fm)
        prey_pop.append(p1)
        predator_pop.append(p2)
    return [prey_pop, predator_pop]


def runge_kutta_midpoint(p1, p2, n, h, k_m, k_mf, k_f, k_fm):
    prey_pop = [p1]
    predator_pop = [p2]
    for i in range(n):
        p1 = p1 + h * prey(p1 + (h / 2 * prey(p1, p2, k_m, k_mf)), p2 + (h / 2 * predator(p1, p2, k_f, k_fm)), k_m, k_mf)
        p2 = p2 + h * predator(p1 + (h / 2 * prey(p1, p2, k_m, k_mf)), p2 + (h / 2 * predator(p1, p2, k_f, k_fm)), k_f,
                               k_fm)
        prey_pop.append(p1)
        predator_pop.append(p2)
    return [prey_pop, predator_pop]


def runge_kutta_4thorder(p1, p2, n, h, k_m, k_mf, k_f, k_fm):
    prey_pop = [p1]
    predator_pop = [p2]

    for i in range(n):
        prey_1 = h * prey(p1, p2, k_m, k_mf)
        predator_1 = h * predator(p1, p2, k_f, k_fm)
        prey_2 = h * prey(p1 + prey_1 / 2, p2 + predator_1 / 2, k_m, k_mf)
        predator_2 = h * predator(p1 + prey_1 / 2, p2 + predator_1 / 2, k_f, k_fm)
        prey_3 = h * prey(p1 + prey_2 / 2, p2 + predator_2 / 2, k_m, k_mf)
        predator_3 = h * predator(p1 + prey_2 / 2, p2 + predator_2 / 2, k_f, k_fm)
        prey_4 = h * prey(p1 + prey_2, p2 + predator_3, k_m, k_mf)
        predator_4 = h * predator(p1 + prey_2, p2 + predator_3, k_f, k_fm)

        p1 += float(prey_1 + 2 * prey_2 + 2 * prey_3 + prey_4) / 6
        p2 += float(predator_1 + 2 * predator_2 + 2 * predator_3 + predator_4) / 6

        prey_pop.append(p1)
        predator_pop.append(p2)

    return [prey_pop, predator_pop]


def main():
    # start values
    k_m = 2
    k_mf = 0.02
    k_fm = 0.01
    k_f = 1.06
    m0 = 100
    f0 = 15
    h = 0.1
    n = 400

    euclid_set = explicit_euler(m0, f0, n, h, k_m, k_mf, k_f, k_fm)
    rkmidpoint_set = runge_kutta_midpoint(m0, f0, n, h, k_m, k_mf, k_f, k_fm)
    rk4_set = runge_kutta_4thorder(m0, f0, n, h, k_m, k_mf, k_f, k_fm)

    fig, ((a, b), (c, d)) = plt.subplots(2, 2, figsize=(25, 22))

    a.plot(euclid_set[0], euclid_set[1], label="population1", color='lightskyblue')
    a.plot(rkmidpoint_set[0], rkmidpoint_set[1], label="population2", color='cornflowerblue')
    a.plot(rk4_set[0], rk4_set[1], label="population3", color='blue')

    a.set_title('Phase Plot')
    a.set_xlabel('prey', fontsize=12)
    a.set_ylabel('predators', fontsize=12)

    b.set_title('Euclid approximation')
    b.plot(euclid_set[0][:181], label='prey', color='darkorange')
    b.plot(euclid_set[1][:181], label='predators', color='red')

    c.set_title('Midpoint Runge-Kutta approximation')
    c.plot(rkmidpoint_set[0][:181], label='prey', color='darkorange')
    c.plot(rkmidpoint_set[1][:181], label='predators', color='red')

    d.set_title('4th order Runge-Kutta approximation')
    d.plot(rk4_set[0][:181], label='prey', color='darkorange')
    d.plot(rk4_set[1][:181], label='predators', color='red')

    plt.savefig('Lotka Volterra.png')
    plt.show()


# main
if __name__ == "__main__":
    main()
