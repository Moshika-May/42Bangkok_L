/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sort_int_tab.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/14 23:21:44 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/15 00:41:03 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

// #include <stdio.h>
void	ft_sort_int_tab(int *tab, int size)
{
	int	i;
	int	j;
	int	idx;
	int	tmp;

	i = 0;
	while (i < size - 1)
	{
		idx = i;
		j = i + 1;
		while (j < size)
		{
			if (tab[j] < tab[idx])
				idx = j;
			j++;
		}
		if (idx != i)
		{
			tmp = tab[i];
			tab[i] = tab[idx];
			tab[idx] = tmp;
		}
		i++;
	}
}
/*
int	main(void)
{
	int	arr[] = {50, 40, 60, 20, 10, 30};
	int	i;

	i = 0;
	while (i != 6)
	{
		printf("%d ", arr[i]);
		i++;
	}
	ft_sort_int_tab(arr, 6);
	i = 0;
	printf("\n");
	while (i != 6)
	{
		printf("%d ", arr[i]);
		i++;
	}
	return (0);
}
*/
