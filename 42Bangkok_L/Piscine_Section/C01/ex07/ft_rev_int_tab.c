/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_rev_int_tab.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/14 22:42:04 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/14 23:04:54 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

// #include <stdio.h>
void	ft_rev_int_tab(int *tab, int size)
{
	int	i;
	int	j;
	int	tmp;

	i = 0;
	j = size - 1;
	while (i < j)
	{
		tmp = tab[i];
		tab[i] = tab[j];
		tab[j] = tmp;
		i++;
		j--;
	}
}
/*
int	main(void)
{
	int	ar[] = {10, 20, 30, 40, 50};
	int	size;
	int	i;

	size = 5;
	i = 0;
	while (i < 5)
	{
		printf("%d ", ar[i]);
		i++;
	}
	ft_rev_int_tab(ar, size);
	printf("\n");
	i = 0;
	while (i < 5)
	{
		printf("%d ", ar[i]);
		i++;
	}
	return (0);
}
*/
