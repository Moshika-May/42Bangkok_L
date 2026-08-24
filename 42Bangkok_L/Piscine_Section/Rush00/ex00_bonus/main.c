/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/11 00:19:25 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/11 13:48:01 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

void	ft_putchar(char c);
// void	rush(int x, int y);
void	rush00(int x, int y);
void	rush01(int x, int y);
void	rush02(int x, int y);
void	rush03(int x, int y);
void	rush04(int x, int y);

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
int	main(int argc, char *argv[])
{
	int	a;
	int	x;
	int	y;

	a = atoi(argv[1]);
	x = atoi(argv[2]);
	y = atoi(argv[3]);
	if (argc != 4)
	{
		return (0);
	}
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
}
