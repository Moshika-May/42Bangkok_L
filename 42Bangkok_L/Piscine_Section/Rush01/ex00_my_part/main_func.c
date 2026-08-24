/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main_func.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/18 16:16:50 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/18 17:59:03 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

void	ft_putstr(char *str);
int		input_validation(char *str);
int		size_count(char *str);

int	main(int argc, char **argv)
{
	if (argc == 2)
	{
		if (input_validation(argv[1]) == 1)
			return (0);
		ft_putstr("Validation pass");
		return (0);
	}
	ft_putstr("argc != 2");
	return (0);
}
