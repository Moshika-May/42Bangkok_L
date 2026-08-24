/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/11 00:19:25 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/11 17:08:58 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

/*This is std main
 int	main(void)
{
	rush(5, 5);
	return (0);
}
*/
// =====================
// argv[0] = program
// argv[1] = (rush)XX
// argv[2] = x values
// argv[3] = y values
void	decision(int a, int x, int y)
{
	if (a == 0)
		rush00(x, y);
	else if (a == 1)
		rush01(x, y);
	else if (a == 2)
		rush02(x, y);
	else if (a == 3)
		rush03(x, y);
	else if (a == 4)
		rush04(x, y);
	else
		ft_putstr("The first digit must be 1, 2, 3 or 4!");
}

int	main(int argc, char *argv[])
{
	int	a;
	int	x;
	int	y;

	if (argc != 4)
	{
		ft_putstr("It must be 4 argument");
		return (0);
	}
	if (ft_str_is_numeric(argv[1]) == 0
		|| ft_str_is_numeric(argv[2]) == 0 || ft_str_is_numeric(argv[3]) == 0)
	{
		ft_putstr("It must be a digit!");
		return (0);
	}
	a = ft_nbr(argv[1]);
	x = ft_nbr(argv[2]);
	y = ft_nbr(argv[3]);
}
