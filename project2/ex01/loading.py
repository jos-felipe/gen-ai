# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    loading.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: josfelip <josfelip@student.42sp.org.br>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/05/26 17:00:36 by frfrey            #+#    #+#              #
#    Updated: 2024/09/23 16:27:20 by josfelip         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import time
from time import sleep


def ft_progress(lst):
    start_time = time.time()
    iter_time = 0
    for i in lst:
        if i == 1:
            iter_time = time.time() - start_time
        filled_length = int(i * 25 / len(lst))
        bar = '#' * filled_length + '-' * (25 - filled_length)
        
        print(
            "\rETA: {:5.2f} [{:>4.0%}] [{}] {}/{} | elapsed time {:.2f}s".format(
                (len(lst) - i) * iter_time,
                i / len(lst),
                bar,
                i + 1,
                len(lst),
                time.time() - start_time
            ),
            end=""
        )
        yield i



def main():
	a_list = range(1000)
	ret = 0
	for elem in ft_progress(a_list):
		ret += (elem + 3) % 5
		sleep(0.01)
	print()
	print(ret)


if __name__ == "__main__":
    main()