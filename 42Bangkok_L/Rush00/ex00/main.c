/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/11 00:19:25 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/11 04:15:48 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

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
int	main(int argc, chr *argv[])
{
	int	a;

	a = *argv[1];
	if (argc < 3 || argc > 3)
	{
		return (0);
	}
	if (a == 0)
		rush00(*argv[2], *argv[3]);
	else if (a == 1)
		rush01(*argv[2], *argv[3]);
	else if (a == 2)
		rush02(*argv[2], *argv[3]);
	else if (a == 3)
		rush03(*argv[2], *argv[3]);
	else if (a == 4)
		rush04(*argv[2], *argv[3]);
}
