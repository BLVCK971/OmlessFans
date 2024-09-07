namespace Omless.Api.Entities;

public class BaseEntity{
	public DateTime CreatedAt { get; set; }
	public DateTime UpdatedAt { get; set; } = DateTime.Now;
	public string CreatedBy { get; set; } = string.Empty;
	public string UpdatedBy { get; set; } = string.Empty;
}
