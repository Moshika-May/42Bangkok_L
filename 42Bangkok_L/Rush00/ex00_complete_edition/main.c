/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: miazanov <miazanov@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/11 00:19:25 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/12 20:19:12 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

void	rush00(int x, int y);
void	rush01(int x, int y);
void	rush02(int x, int y);
void	rush03(int x, int y);
void	rush04(int x, int y);
void	ft_putchar(char c);
void	ft_putstr(char *str);
int		ft_nbr(char *s);
int		ft_str_is_numeric(char *str);
void	decision(int a, int x, int y);

int	main(int argc, char *argv[])
{
	int	a;
	int	x;
	int	y;

	if (argc == 1)
		rush03(16, 16);
	else
	{
		if (argc != 4)
		{
			ft_putstr("It must be 3 argument");
			return (0);
		}
		if (ft_str_is_numeric(argv[1]) == 0 || ft_str_is_numeric(argv[2]) == 0
			|| ft_str_is_numeric(argv[3]) == 0)
		{
			ft_putstr("It must be a digit!");
			return (0);
		}
		a = ft_nbr(argv[1]);
		x = ft_nbr(argv[2]);
		y = ft_nbr(argv[3]);
		decision(a, x, y);
	}
}
