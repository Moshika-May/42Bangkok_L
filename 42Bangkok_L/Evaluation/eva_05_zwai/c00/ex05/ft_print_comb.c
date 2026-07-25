/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_comb.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/08 19:37:11 by zwai              #+#    #+#             */
/*   Updated: 2026/07/09 12:51:41 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

void	ft_print_comb(void)
{
	char	first_digit;
	char	second_digit;
	char	third_digit;

	first_digit = '0';
	while (first_digit <= '7')
	{
		second_digit = first_digit + 1;
		while (second_digit <= '8')
		{
			third_digit = second_digit + 1;
			while (third_digit <= '9')
			{
				write(1, &first_digit, 1);
				write(1, &second_digit, 1);
				write(1, &third_digit, 1);
				third_digit++;
			}
			second_digit++;
		}
		first_digit++;
	}
}

int	main(void)
{
	ft_print_comb();
	return (0);
}
